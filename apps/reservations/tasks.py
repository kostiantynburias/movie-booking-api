from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from apps.reservations.models import Reservation


@shared_task
def cleanup_expired_reservations():
    """Batch delete expired pending reservations (older than 15 minutes)."""
    expiration_time = timezone.now() - timedelta(minutes=15)

    expired_queryset = Reservation.objects.filter(
        status=Reservation.StatusChoices.PENDING,
        created_at__lte=expiration_time
    )

    count, _ = expired_queryset.delete()
    return f"Successfully cleaned up {count} expired objects."


@shared_task
def send_ticket_email_task(reservation_id):
    """Generate and send confirmation email with ticket details after status set to confirmed"""
    try:
        reservation = Reservation.objects.select_related(
            'user', 'showtime', 'showtime__movie'
        ).prefetch_related('tickets__seat').get(id=reservation_id)
    except Reservation.DoesNotExist:
        return f"Reservation {reservation_id} not found."

    seats_info = ", ".join([
        f"Ряд {t.seat.row_number}, Місце {t.seat.seat_number}" 
        for t in reservation.tickets.all()
    ])

    subject = f"Квитки на фільм {reservation.showtime.movie.title}"
    message = (
        f"Вітаємо, {reservation.user.username}!\n\n"
        f"Ваше бронювання №{reservation.id} успішно підтверджено.\n"
        f"Фільм: {reservation.showtime.movie.title}\n"
        f"Час: {reservation.showtime.start_time.strftime('%Y-%m-%d %H:%M')}\n"
        f"Місця: {seats_info}\n\n"
        f"Дякуємо, що обираєте наш кінотеатр!"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@cinema.com'),
        recipient_list=[reservation.user.email],
        fail_silently=False,
    )

    return f"Email sent successfully for reservation {reservation_id}."