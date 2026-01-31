# 🎬 VellaVision — Django Full Stack Project

![Python](https://img.shields.io/badge/Python-3.13+-blue)
![Django](https://img.shields.io/badge/Django-6.x-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A **full‑stack YouTube‑like video sharing platform** built with **Django**, focused on clean architecture, security, and a **Gen‑Z inspired modern UI**.

This project demonstrates **real‑world Django development**, including authentication, media handling, CSRF protection, and responsive UI design.

---

## 🚀 Key Features

- 🔐 Secure Authentication (Register, Login, Logout)
- 🎥 Video Upload with Thumbnail Support
- 📃 Video Listing Feed (YouTube‑style)
- 👤 User Profiles & Ownership
- 🎨 Gen‑Z UI (Glassmorphism + Neon Accents)
- 🛡️ CSRF & Security Best Practices
- 📱 Mobile‑Responsive Layout

---

## 🛠️ Tech Stack

| Layer | Technology |
|-----|-----------|
| Backend | Django 6.x |
| Frontend | HTML5, CSS3 (Custom UI), JavaScript |
| Database | SQLite (Dev) |
| Auth | Django Auth |
| Media | Django Media Files |
| Tooling | uv, Git |
| Python | 3.13+ |

---

## 📁 Project Structure

```
D:.
│   db.sqlite3
│   manage.py
│
├───accounts
│   │   admin.py
│   │   apps.py
│   │   forms.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   ├───migrations
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           __init__.cpython-313.pyc
│   │
│   ├───templates
│   │   └───accounts
│   │           logged_out.html
│   │           login.html
│   │           register.html
│   │
│   └───__pycache__
│           admin.cpython-313.pyc
│           apps.cpython-313.pyc
│           forms.cpython-313.pyc
│           models.cpython-313.pyc
│           urls.cpython-313.pyc
│           views.cpython-313.pyc
│           __init__.cpython-313.pyc
│
├───static
│   └───css
│           auth.css
│           base.css
│           buttons.css
│           forms.css
│           messages.css
│           navbar.css
│           upload.css
│           variables.css
│           videoplayer.css
│           videos.css
│
├───templates
│       base.html
│
├───videos
│   │   admin.py
│   │   apps.py
│   │   forms.py
│   │   imagekit_client.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   ├───migrations
│   │   │   0001_initial.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           0001_initial.cpython-313.pyc
│   │           __init__.cpython-313.pyc
│   │
│   ├───templates
│   │   └───videos
│   │           channel.html
│   │           detail.html
│   │           list.html
│   │           upload.html
│   │
│   └───__pycache__
│           admin.cpython-313.pyc
│           apps.cpython-313.pyc
│           forms.cpython-313.pyc
│           imagekit_client.cpython-313.pyc
│           models.cpython-313.pyc
│           urls.cpython-313.pyc
│           views.cpython-313.pyc
│           __init__.cpython-313.pyc
│
└───youtube
    │   .env
    │   asgi.py
    │   settings.py
    │   urls.py
    │   wsgi.py
    │   __init__.py
    │
    └───__pycache__
            settings.cpython-313.pyc
            urls.cpython-313.pyc
            wsgi.cpython-313.pyc
            __init__.cpython-313.pyc

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/youtube-clone.git
cd youtube-clone
```

### 2️⃣ Install Dependencies
```bash
uv sync
```

### 3️⃣ Run Migrations
```bash
uv run python manage.py migrate
```

### 4️⃣ Create Superuser (Optional)
```bash
uv run python manage.py createsuperuser
```

### 5️⃣ Run Server
```bash
uv run python manage.py runserver
```

Visit 👉 `http://127.0.0.1:8000/`

---

## 🔐 Environment Variables

Create a `.env` file (not committed):

```env
DEBUG=True
SECRET_KEY=your-secret-key
```

---

## 🖼️ Screenshots

> Add screenshots here for GitHub:
```
/screenshots
├── home.png
├── login.png
├── register.png
├── upload.png
```

```md
![Home](screenshots/home.png)
![Login](screenshots/login.png)
![Register](screenshots/register.png)
![Upload](screenshots/upload.png)
![VideoPlayer](screenshots/videoplayer.png)
---

## 📌 Future Enhancements

- 💬 Comments & Likes
- 📊 View Count Analytics
- 🔔 Channel Subscriptions
- ☁️ Cloud Video Storage (AWS / Cloudinary)
- 🎞️ Video Streaming Optimization

---

## 🎯 Resume‑Ready Project Description

> **VellaVision(Django)**  
Developed a full‑stack video‑sharing platform using Django with secure authentication, media uploads, CSRF protection, and a modern responsive UI. Implemented clean URL routing, reusable apps, and production‑ready project structure.

---

## 👨‍💻 Author

**Soumyaranjan Pradhan**  
MCA Student | Python Full‑Stack Developer  

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub — it really helps!
