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
* **Database:** PostgreSQL 17
* **Containerization:** Docker, Docker Compose
* **Environment Management:** `python-dotenv`
* **Planned Extensions:** Celery, Redis (for async ticket delivery & reservation cleanup)

---

## 🖼 Demo & Documentation

> 🌐 **Live Demo:** Work in progress (Will be deployed upon API completion)  
> 📑 **API Documentation:** Swagger / ReDoc OpenAPI endpoints will be available at `/api/docs/`

---

## ✨ Features & Architecture Roadmap

* [x] **Docker Infrastructure:** Containerized environment with PostgreSQL and Django Web service.
* [x] **Project Core Setup:** Configured environment variables, Database settings, and Security options.
* [ ] **Custom User Model & Auth:** JWT-based authentication with Role-Based Access Control (Admin / Customer).
* [ ] **Movie & Showtime Management:** Automated overlap validation calculating movie runtime + 20-min mandatory hall cleaning break.
* [ ] **Atomic Reservation Logic:** Concurrency control (`transaction.atomic()` + `select_for_update()`) with `UniqueConstraint(showtime, seat)` to guarantee 100% protection against double-booking.
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
├── apps/                   # Custom Django apps (In development)
├── core/                   # Project configuration & settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env                    # Environment variables (git-ignored)
├── .env.example            # Environment template for development
├── .gitignore              # Git ignore rules
├── docker-compose.yml      # Multi-container orchestration
├── Dockerfile              # Container image build configuration
├── LICENSE                 # MIT License file
├── manage.py               # Django management script
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```
---

## 📄 License

This project is open-source software licensed under the [MIT License](LICENSE).

---

## 📬 Contact & Links

* **GitHub:** [@kostiantynburias](https://github.com/kostiantynburias)
* **Email:** bloodyaresyt@gmail.com
* **Telegram:** [@His_Majesty_Qin](https://t.me/His_Majesty_Qin)