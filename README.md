# Zomato-like Food Delivery App

A comprehensive food delivery application built with Flask, MySQL, and modern web technologies. This project demonstrates full-stack development with authentication, order management, analytics, and responsive UI.

## Features

### 🍽️ **Core Features**
- **User Authentication**: Secure login/register with password hashing
- **Menu Management**: Dynamic menu with categories, pricing, and food images
- **Menu Administration**: Add, edit, delete menu items with search and filtering
- **Order System**: Real-time cart, order placement, and tracking
- **Order Management**: View, edit, and delete orders with filtering
- **Analytics Dashboard**: Charts and statistics for business insights
- **Category Filtering**: Filter menu items by category on the home page

### 🛡️ **Security Features**
- CSRF protection with Flask-WTF
- Password hashing with Werkzeug
- Session-based authentication
- Input validation and sanitization
- SQL injection prevention

### 📊 **Analytics & Reporting**
- Total orders count
- Most popular dishes (top 5)
- Orders per day (past 7 days)
- Orders by category (pie chart)
- Interactive charts with Chart.js
- Real-time data updates

### 🎨 **UI/UX Features**
- Responsive design with Bootstrap 5
- Modern card-based layout
- Dynamic cart preview
- Real-time form validation
- Toast notifications
- Loading states and animations
- Mobile-friendly interface

## Technology Stack

### Backend
- **Flask**: Web framework
- **MySQL**: Database
- **Flask-WTF**: CSRF protection and forms
- **Werkzeug**: Password hashing
- **python-dotenv**: Environment variables

### Frontend
- **Bootstrap 5**: CSS framework
- **Chart.js**: Data visualization
- **jQuery**: DOM manipulation
- **Font Awesome**: Icons

### Database
- **MySQL**: Relational database
- **Connection Pooling**: Performance optimization
- **Foreign Keys**: Data integrity

## Project Structure

```
zomato_data_engineering-main/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── init_db.py           # Database initialization
├── migrate_db.py        # Database migration script
├── setup.py             # Setup script
├── README.md            # This file
├── models/              # Database models
│   ├── __init__.py
│   ├── database.py      # Database connection manager
│   ├── user.py          # User model and authentication
│   ├── order.py         # Order model and analytics
│   └── item.py          # Menu item model
├── routes/              # Flask routes
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   ├── orders.py        # Order management routes
│   ├── analytics.py     # Analytics routes
│   └── menu.py          # Menu management routes
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── home.html        # Menu and ordering
│   ├── orders.html      # Order history
│   ├── analytics.html   # Analytics dashboard
│   ├── edit_order.html  # Edit order form
│   └── menu/            # Menu management templates
│       └── manage_menu.html
│   └── errors/          # Error pages
│       ├── 404.html
│       ├── 500.html
│       └── 403.html
└── static/              # Static files
    ├── css/
    │   └── style.css    # Custom styles
    └── js/
        └── main.js      # Main JavaScript
```

## New Features (Latest Update)

### 🆕 **Menu Management System**
- **Add New Items**: Create menu items with name, category, price, and image URL
- **Edit Items**: Update existing menu items with real-time validation
- **Delete Items**: Remove menu items with confirmation dialogs
- **Search & Filter**: Find items by name or filter by category
- **Image Support**: Display food images from URLs in menu cards

### 🎨 **Enhanced UI/UX**
- **Category Filtering**: Filter menu items by category on the home page
- **Food Images**: Beautiful food images displayed in menu cards
- **Modern Design**: Updated Bootstrap 5 components with custom styling
- **Responsive Layout**: Mobile-friendly design with improved navigation
- **Interactive Elements**: Hover effects, animations, and smooth transitions

### 🔧 **Database Improvements**
- **Image URL Column**: Added `image_url` field to items table
- **Rich Menu Data**: 16 realistic menu items with high-quality images
- **Migration Script**: Automated database schema updates
- **Setup Automation**: One-command setup with `python setup.py`

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd zomato_data_engineering-main
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup

#### Option A: Using setup.py (Recommended)
```bash
python setup.py
```
This will automatically:
- Create a default `.env` file if it doesn't exist
- Initialize the database with tables and sample data
- Run database migrations to add new features
- Update existing items with image URLs

#### Option B: Manual Setup
1. Create MySQL database:
```sql
CREATE DATABASE zomato;
```

2. Run the initialization script:
```bash
python init_db.py
```

3. Run the migration script:
```bash
python migrate_db.py
```

### Step 5: Environment Configuration
Create a `.env` file in the root directory:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=zomato
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
```

### Step 6: Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

### Demo Credentials
- **Username**: alice, bob, or charlie
- **Password**: password123

### Features Walkthrough

1. **Authentication**
   - Register a new account or login with demo credentials
   - Secure password hashing and session management

2. **Menu & Ordering**
   - Browse menu items organized by category with beautiful food images
   - Filter items by category using the filter buttons
   - Add items to cart with quantity controls
   - Real-time cart preview with total calculation
   - Place orders with delivery address

3. **Menu Management** (New!)
   - Access menu management at `/menu/menu`
   - Add new menu items with name, category, price, and image URL
   - Edit existing items with real-time validation
   - Delete items with confirmation dialogs
   - Search items by name or filter by category

4. **Order Management**
   - View order history with filtering options
   - Filter by date range and dish name
   - Sort by latest orders, dish name, or quantity
   - Edit order quantities and delivery addresses
   - Delete orders with confirmation

5. **Analytics Dashboard**
   - View total orders and business metrics
   - Interactive charts for popular dishes
   - Orders per day trend analysis
   - Category-wise order distribution
   - Real-time data updates

## API Endpoints

### Authentication
- `GET /auth/login` - Login page
- `POST /auth/login` - Login form submission
- `GET /auth/register` - Registration page
- `POST /auth/register` - Registration form submission
- `GET /auth/logout` - Logout

### Orders
- `GET /orders/` - Home page with menu
- `POST /orders/place_order` - Place new order
- `GET /orders/view_orders` - View user orders
- `GET /orders/all_orders` - View all orders (admin)
- `POST /orders/delete_order/<id>` - Delete order
- `GET /orders/edit_order/<id>` - Edit order form
- `POST /orders/edit_order/<id>` - Update order

### Analytics
- `GET /analytics/analytics` - Analytics dashboard
- `GET /api/analytics/popular_dishes` - Popular dishes data
- `GET /api/analytics/orders_per_day` - Orders per day data
- `GET /api/analytics/orders_by_category` - Category data
- `GET /api/analytics/summary` - Analytics summary

### Menu Management
- `GET /menu/menu` - Menu management page
- `POST /menu/menu/add` - Add new menu item
- `PUT /menu/menu/edit/<id>` - Edit menu item
- `DELETE /menu/menu/delete/<id>` - Delete menu item
- `GET /menu/menu/categories` - Get all categories

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
    price DECIMAL(10,2)
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

## Security Features

### Input Validation
- Username: 3-50 characters, alphanumeric + underscore
- Password: Minimum 6 characters
- Quantity: 1-100 range
- Address: Minimum 10 characters, HTML sanitization

### Authentication
- Password hashing with Werkzeug
- Session-based authentication
- CSRF protection on all forms
- Login required decorator for protected routes

### Database Security
- Parameterized queries to prevent SQL injection
- Connection pooling for performance
- Foreign key constraints for data integrity
- Error handling and logging

## Performance Optimizations

### Database
- Connection pooling (5 connections)
- Indexed foreign keys
- Optimized queries with JOINs
- Transaction management

### Frontend
- Minified CSS and JavaScript
- CDN resources (Bootstrap, Chart.js)
- Lazy loading for charts
- Debounced search inputs

### Caching
- Session-based user data
- Chart data caching
- Static file caching headers

## Deployment

### Production Considerations
1. **Environment Variables**: Update `.env` with production values
2. **Database**: Use production MySQL instance
3. **Secret Key**: Generate strong secret key
4. **HTTPS**: Enable SSL/TLS
5. **Logging**: Configure proper logging
6. **Monitoring**: Add health checks and monitoring

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Feel free to use and modify as needed.

## Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

---

**Happy Coding! 🚀**
