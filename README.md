# Zomato-like Food Delivery App

A comprehensive food delivery application built with **Flask**, **MySQL**, and modern web technologies. This project demonstrates full‑stack development with authentication, order management, analytics, and a responsive UI.

---

## Table of Contents

* [Features](#features)

  * [Core Features](#-core-features)
  * [Security Features](#-security-features)
  * [Analytics & Reporting](#-analytics--reporting)
  * [UI/UX Features](#-uiux-features)
* [Technology Stack](#technology-stack)
* [Project Structure](#project-structure)
* [New Features (Latest Update)](#new-features-latest-update)
* [Installation & Setup](#installation--setup)

  * [Prerequisites](#prerequisites)
  * [Quick Start](#quick-start)
  * [Environment Configuration](#environment-configuration)
* [Usage](#usage)
* [API Endpoints](#api-endpoints)
* [Database Schema](#database-schema)
* [Security Features](#security-features-1)
* [Performance Optimizations](#performance-optimizations)
* [Deployment](#deployment)
* [Contributing](#contributing)
* [License](#license)
* [Support](#support)

---

## Features

### 🍽️ Core Features

* **User Authentication** — Secure login/register with password hashing
* **Menu Management** — Dynamic menu with categories, pricing, and food images
* **Menu Administration** — Add, edit, delete menu items with search & filtering
* **Order System** — Real-time cart, order placement, and tracking
* **Order Management** — View, edit, and delete orders with filters
* **Analytics Dashboard** — Charts and statistics for business insights
* **Category Filtering** — Filter menu items by category on the home page

### 🛡️ Security Features

* CSRF protection with `Flask-WTF`
* Password hashing with `Werkzeug`
* Session-based authentication
* Input validation and sanitization
* Parameterized queries (prevents SQL injection)

### 📊 Analytics & Reporting

* Total orders count
* Most popular dishes (top 5)
* Orders per day (past 7 days)
* Orders by category (pie chart)
* Interactive charts powered by `Chart.js`
* Real-time data updates

### 🎨 UI/UX Features

* Responsive design with `Bootstrap 5`
* Modern card-based layout
* Dynamic cart preview
* Real-time form validation and toast notifications
* Loading states, animations and mobile-friendly interface

---

## Technology Stack

**Backend**

* Flask, Flask-WTF, Werkzeug, python-dotenv

**Frontend**

* Bootstrap 5, Chart.js, jQuery, Font Awesome

**Database**

* MySQL with connection pooling and foreign keys for integrity

---

## Project Structure

```
zomato_data_engineering-main/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── init_db.py             # Database initialization
├── migrate_db.py          # Database migration script
├── setup.py               # Setup script
├── README.md              # This file
├── models/                # Database models
│   ├── __init__.py
│   ├── database.py        # DB connection manager
│   ├── user.py            # User model & auth
│   ├── order.py           # Order model & analytics
│   └── item.py            # Menu item model
├── routes/                # Flask routes
│   ├── __init__.py
│   ├── auth.py            # Authentication routes
│   ├── orders.py          # Order management routes
│   ├── analytics.py       # Analytics routes
│   └── menu.py            # Menu management routes
├── templates/             # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   ├── orders.html
│   ├── analytics.html
│   ├── edit_order.html
│   └── menu/
│       └── manage_menu.html
│   └── errors/
│       ├── 404.html
│       ├── 500.html
│       └── 403.html
└── static/                # Static files
    ├── css/
    │   └── style.css      # Custom styles
    └── js/
        └── main.js        # Main JavaScript
```

---

## New Features (Latest Update)

### 🆕 Menu Management System

* Add, edit and delete menu items (name, category, price, image URL)
* Real-time validation when editing
* Search & filter by name/category
* Image support via `image_url` field

### 🎨 Enhanced UI/UX

* Better category filtering and food image display
* Modernized Bootstrap 5 components and responsive styling
* Interactive elements (hover effects, animations)

### 🔧 Database Improvements

* `image_url` column for items
* 16 sample menu items with image URLs
* Migration script and one-command setup (`python setup.py`)

---

## Installation & Setup

### Prerequisites

* Python 3.8+
* MySQL 8.0+
* `pip`

### Quick Start

```bash
git clone <repository-url>
cd zomato_data_engineering-main
```

Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

#### Option A — Recommended: Automated setup

```bash
python setup.py
```

This will:

* Create a default `.env` if missing
* Initialize DB and sample data
* Run migrations to add new features
* Update items with image URLs

#### Option B — Manual setup

1. Create database:

```sql
CREATE DATABASE zomato;
```

2. Initialize DB:

```bash
python init_db.py
```

3. Run migrations:

```bash
python migrate_db.py
```

### Environment Configuration

Create a `.env` file at project root:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=zomato
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
```

### Run the App

```bash
python app.py
```

Visit `http://localhost:5000`

---

## Usage

**Demo Credentials**

* Username: `alice`, `bob`, or `charlie`
* Password: `password123`

**Walkthrough**

* Register/login (secure password hashing & session management)
* Browse menu with categories and images
* Add items to cart, adjust quantities, place orders
* Access menu management at `/menu/menu` to add/edit/delete items
* View analytics at `/analytics/analytics`

---

## API Endpoints

### Authentication

* `GET /auth/login` — Login page
* `POST /auth/login` — Login submission
* `GET /auth/register` — Registration page
* `POST /auth/register` — Registration submission
* `GET /auth/logout` — Logout

### Orders

* `GET /orders/` — Home/menu page
* `POST /orders/place_order` — Place new order
* `GET /orders/view_orders` — View user orders
* `GET /orders/all_orders` — View all orders (admin)
* `POST /orders/delete_order/<id>` — Delete order
* `GET /orders/edit_order/<id>` — Edit order form
* `POST /orders/edit_order/<id>` — Update order

### Analytics

* `GET /analytics/analytics` — Analytics dashboard
* `GET /api/analytics/popular_dishes` — Popular dishes data
* `GET /api/analytics/orders_per_day` — Orders per day data
* `GET /api/analytics/orders_by_category` — Category distribution
* `GET /api/analytics/summary` — Summary stats

### Menu Management

* `GET /menu/menu` — Menu management page
* `POST /menu/menu/add` — Add new menu item
* `PUT /menu/menu/edit/<id>` — Edit menu item
* `DELETE /menu/menu/delete/<id>` — Delete menu item
* `GET /menu/menu/categories` — Get all categories

---

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Items Table

```sql
CREATE TABLE items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50),
    price DECIMAL(10,2),
    image_url VARCHAR(255)
);
```

### Orders Table

```sql
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    delivery_address TEXT NOT NULL,
    order_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
);
```

---

## Security Features

### Input Validation

* Username: 3–50 chars, alphanumeric + underscore
* Password: Minimum 6 characters
* Quantity: 1–100
* Address: Minimum 10 characters, HTML sanitization

### Authentication & DB Security

* Password hashing (Werkzeug)
* CSRF protection on all forms
* Login required decorator for protected routes
* Parameterized queries and foreign key constraints

---

## Performance Optimizations

### Database

* Connection pooling (default 5 connections)
* Indexed foreign keys
* Optimized queries with JOINs and transactions

### Frontend

* Minified CSS/JS
* CDN for Bootstrap and Chart.js
* Lazy-loading charts and debounced search inputs

### Caching

* Session caching for user data
* Chart data caching
* Static file caching headers

---

## Deployment

### Production Checklist

1. Set production environment variables in `.env`
2. Use a managed MySQL instance
3. Generate a strong `SECRET_KEY`
4. Enable HTTPS (SSL/TLS)
5. Configure logging and monitoring
6. Add health checks

### Docker (Optional)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

---

## Contributing

1. Fork the repo
2. Create a feature branch
3. Make changes and add tests where applicable
4. Submit a pull request

---

## License

This project is for educational purposes. Feel free to use and modify as needed.

---

## Support

1. Check the documentation
2. Review existing issues
3. Create a new issue with a clear title and reproduction steps

---

**Happy Coding! 🚀**
