# 🎬 Movie Booking API

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🛠 **Project Status:** In Active Development (Work in Progress)

A RESTful API for managing single-hall cinema movie screenings, seat reservations, and user bookings. Built with Django and PostgreSQL, containerized with Docker, and engineered with protection against race conditions and double-booking.

---

## 🛠 Tech Stack

* **Backend Framework:** Python 3.12, Django, Django REST Framework (DRF)
* **Authentication:** SimpleJWT (JSON Web Tokens)
* **API Documentation:** `drf-spectacular` (OpenAPI 3.0, Swagger UI & ReDoc)
* **Database:** PostgreSQL 17
* **Containerization:** Docker, Docker Compose
* **Environment Management:** `python-dotenv`
* **Planned Extensions:** Celery, Redis (for async ticket delivery & reservation cleanup)

---

## 🖼 Demo & Documentation

> 🌐 **Live Demo:** Work in progress (Will be deployed upon API completion)  
> 📑 **API Documentation:** Interactive Swagger UI is available at `/api/v1/docs/` and ReDoc at `/api/v1/redoc/`

---

## ✨ Features & Architecture Roadmap

* [x] **Docker Infrastructure:** Containerized environment with PostgreSQL and Django Web service.
* [x] **Project Core Setup:** Configured environment variables, Database settings, and Security options.
* [x] **Custom User Model & Auth:** JWT-based authentication, registration, user profile management, password change, and Role-Based Access Control (Admin / Customer).
* [x] **API Auto-Documentation:** OpenAPI 3.0 integration with Swagger UI (`drf-spectacular`).
* [x] **Movie & Genre Management:** CRUD operations for movies and genres with `django-filter` support.
* [x] **Showtimes & Overlap Validation:** Automated screening overlap calculation considering movie runtime + 20-min mandatory hall cleaning break.
* [x] **Atomic Reservation Logic:** Concurrency control (`transaction.atomic()` + `select_for_update()`) with `UniqueConstraint(showtime, seat)` to guarantee 100% protection against double-booking.
* [ ] **Background Processing:** Celery tasks for auto-expiring 15-min unconfirmed holds and rendering PDF tickets.

---

## 🚀 Getting Started Locally

### Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with Docker Compose) installed.
* [Git](https://git-scm.com/) installed.

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kostiantynburias/movie-booking-api.git .
   ```

2. **Configure Environment Variables:** Create a `.env` file in the project root based on `.env.example`:
   ```env
   # Django Settings
   SECRET_KEY=your-django-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost,web,cinema-backend

   # Database Settings (PostgreSQL)
   POSTGRES_DB=cinema_db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=db
   POSTGRES_PORT=5432

   # Redis Connection URL
   REDIS_URL=redis://redis:6379/0

   # Email SMTP
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL="Cinema Booking <your-email@gmail.com>"
   ```

3. **Build and Start Containers:** Run Docker Compose to build images and launch services in detached mode:
   ```bash
   docker compose up -d --build
   ```

4. **Apply Database Migrations:**
   ```bash
   docker compose exec web python manage.py migrate
   ```

5. **Create Superuser (Admin Access):**
   ```bash
   docker compose exec -it web python manage.py createsuperuser
   ```

6. **Access Services:**
   * **API Base URL:** `http://localhost:8000/`
   * **Django Admin Panel:** `http://localhost:8000/admin/`

---

## 📂 Current Project Structure

```text
movie-booking-api/
├── apps/                    # Custom Django applications
│   ├── movies/              # Movie & Genre management
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── filters.py       # Custom MovieFilter (genres, duration, title search)
│   │   ├── models.py
│   │   ├── serializers.py   # Genre & Movie serializers
│   │   ├── tests.py
│   │   ├── urls.py          # Movies API endpoints routing
│   │   └── views.py         # GenreViewSet & MovieViewSet
│   ├── reservations/        # Reservations & Ticket management
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py        # Reservation, Ticket, Seat models
│   │   ├── serializers.py   # Base, Detail, List, Admin & Create serializers
│   │   ├── tasks.py         # Celery tasks (e.g., send_ticket_email_task)
│   │   ├── tests.py
│   │   ├── urls.py          # Customer profile & Admin reservation endpoints
│   │   └── views.py         # UserReservationsViewSet & AdminReservationsViewSet
│   ├── showtimes/           # Showtimes & Schedule management
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── filters.py       # ShowtimeFilter (filter by date, movie)
│   │   ├── models.py        # Showtime model with 20-min cleaning break validation
│   │   ├── serializers.py   # Showtime serializers
│   │   ├── tests.py
│   │   ├── urls.py          # Showtimes API endpoints routing
│   │   └── views.py         # ShowtimeViewSet
│   └── users/               # Authentication & User Management
│       ├── admin.py
│       ├── apps.py
│       ├── models.py        # CustomUser model (Email-based auth)
│       ├── serializers.py   # Registration, Profile & Password Change serializers
│       ├── tests.py
│       ├── urls.py          # Auth API endpoints routing
│       └── views.py         # Auth & User Profile views
├── core/                    # Root project configuration
│   ├── asgi.py
│   ├── celery.py            # Celery app instance and configuration
│   ├── permissions.py       # Custom IsAdminOrReadOnly permission
│   ├── settings.py          # Application settings & third-party packages config
│   ├── urls.py              # Root URL routing & OpenAPI docs (Swagger/ReDoc)
│   └── wsgi.py
├── media/                   # User-uploaded media files
├── .env                     # Local environment variables (git-ignored)
├── .env.example             # Environment template
├── .gitignore
├── docker-compose.yml       # Multi-container orchestration
├── Dockerfile               # Container build configuration
├── LICENSE                  # MIT License
├── manage.py
├── README.md
└── requirements.txt         # Project dependencies
```
---

## 📄 License

This project is open-source software licensed under the [MIT License](LICENSE).

---

## 📬 Contact & Links

* **GitHub:** [@kostiantynburias](https://github.com/kostiantynburias)
* **Email:** bloodyaresyt@gmail.com
* **Telegram:** [@His_Majesty_Qin](https://t.me/His_Majesty_Qin)