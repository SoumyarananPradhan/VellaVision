# 🎬 VellaVision — Django Full Stack Project

![Python](https://img.shields.io/badge/Python-3.13+-blue)
![Django](https://img.shields.io/badge/Django-6.x-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Production-336791)
![Cloudinary](https://img.shields.io/badge/Cloudinary-Media_Storage-orange)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A **full‑stack YouTube‑like video sharing platform** built with **Django**, focused on clean architecture, security, and a **Gen‑Z inspired modern UI**.

This project demonstrates **real‑world Django development**, including authentication, permanent cloud media handling (Cloudinary), production database integration (PostgreSQL), and responsive UI design.

---

## 🚀 Key Features

- 🔐 Secure Authentication (Register, Login, Logout)
- ☁️ Cloudinary Integration (Permanent Video & Thumbnail Storage)
- 🎥 Video Upload with Auto-generated Thumbnails
- 📃 Video Listing Feed (YouTube‑style)
- 👤 User Profiles & Ownership
- 🎨 Gen‑Z UI (Glassmorphism + Neon Accents)
- 🛡️ CSRF & Security Best Practices
- 🚀 Production Ready (Configured for Railway/PostgreSQL)

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|------------|
| Backend | Django 6.0+ |
| Frontend | HTML5, CSS3, JavaScript |
| Database | PostgreSQL (Production) / SQLite (Local) |
| Storage | Cloudinary |
| Tooling | uv, Git, Docker |
| Deployment | Railway |

---

## 📁 Project Structure

```text
D:.
│   db.sqlite3
│   manage.py
│   requirements.txt
│   Dockerfile
│
├── accounts/
├── static/
│   └── css/
├── templates/
├── videos/
│   └── templates/videos/
└── youtube/
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/SoumyarananPradhan/VellaVision.git
cd VellaVision
```

### 2️⃣ Install Dependencies
```bash
uv sync
# or
pip install -r requirements.txt
```

### 3️⃣ Configure Environment
Create a `.env` file inside `youtube/`:

```env
DEBUG=True
SECRET_KEY=your-secret-key

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 4️⃣ Run Migrations
```bash
uv run python manage.py migrate
```

### 5️⃣ Create Superuser
```bash
uv run python manage.py createsuperuser
```

### 6️⃣ Run Server
```bash
uv run python manage.py runserver
```

Visit: http://127.0.0.1:8000/

---

## ☁️ Deployment (Railway)

- Push to GitHub
- Connect repo to Railway
- Add PostgreSQL service
- Set environment variables:
  - SECRET_KEY
  - DEBUG=False
  - CLOUDINARY keys
  - CSRF_TRUSTED_ORIGINS

---

## 📌 Future Enhancements

- 💬 Comments System
- 📊 Analytics & Watch History
- 🔔 Channel Subscriptions
- 🎞️ HLS Streaming

---

## 👨‍💻 Author

**Soumyaranjan Pradhan**  
MCA Student | Python Full‑Stack Developer

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
