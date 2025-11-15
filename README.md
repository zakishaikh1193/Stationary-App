# 📚 Student Stationery Shop

A modern e-commerce web application for managing and selling student stationery products. Built with Flask backend and vanilla JavaScript frontend.

## ✨ Features

### 🛍️ Shopping Features
- **Product Catalog**: Browse all available stationery products with beautiful card layouts
- **Search & Filter**: Find products by name or filter by category
- **Product Details**: View detailed product information in a modal
- **Shopping Cart**: Add products to cart, update quantities, and checkout
- **Order Management**: Complete checkout process with order creation
- **Order History**: View all past orders with detailed item information
- **Success Popup**: Beautiful confirmation popup after successful checkout
- **Real-time Cart Badge**: See cart item count in the navigation bar

### ⚙️ Admin Features
- **Product Management**: Full CRUD operations (Create, Read, Update, Delete)
- **Inventory Tracking**: Monitor stock levels with visual indicators
- **Modern UI**: Intuitive admin panel with responsive data table

### 🎨 UI/UX Highlights
- **Modern Design**: Beautiful gradient backgrounds and card-based layouts
- **Responsive**: Works seamlessly on desktop, tablet, and mobile devices
- **Smooth Animations**: Hover effects, transitions, and loading states
- **Toast Notifications**: User-friendly feedback for all actions
- **Modal Dialogs**: Clean forms for adding/editing products

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- MySQL Server
- Modern web browser

### Installation

1. **Clone the repository**
```bash
cd "Project (3)"
```

2. **Install Python dependencies**
```bash
pip install flask flask-cors mysql-connector-python werkzeug
```

3. **Set up MySQL Database**
   - Make sure MySQL server is running
   - The application will automatically create the database and tables

4. **Configure Environment Variables** (Optional)
   
   You can set these environment variables or use the defaults:
   ```bash
   # MySQL Configuration
   MYSQL_HOST=127.0.0.1
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=app_db
   
   # Flask Configuration
   FLASK_RUN_HOST=127.0.0.1
   FLASK_RUN_PORT=5000
   SECRET_KEY=your-secret-key-here
   ```

5. **Initialize the database with sample data**
```bash
python seed_products.py
```

6. **Start the Flask backend**
```bash
cd backend
python run.py
```

   The server will start at `http://127.0.0.1:5000`

7. **Open the frontend**
   - Open `index.html` in your web browser, or
   - Use a local server like Live Server (VS Code extension)

## 📁 Project Structure

```
Project (3)/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── db.py          # Database operations
│   │   │   └── user.py        # User model
│   │   └── routes/
│   │       ├── auth.py        # Authentication routes
│   │       ├── products.py    # Product CRUD APIs
│   │       ├── cart.py        # Shopping cart APIs
│   │       ├── orders.py      # Order management APIs
│   │       └── main.py        # Main routes
│   ├── config.py              # Configuration
│   └── run.py                 # Application entry point
├── index.html                 # Home page
├── shop.html                  # Product catalog page
├── admin.html                 # Admin panel for product management
├── cart.html                  # Shopping cart page
├── orders.html                # Order history page
├── register.html              # User registration
├── shop.js                    # Shop page logic
├── admin.js                   # Admin panel logic
├── cart.js                    # Cart page logic
├── orders.js                  # Orders page logic
├── style.css                  # Main stylesheet
├── seed_products.py           # Database seeder script
└── README.md                  # This file
```

## 🔌 API Endpoints

### Products
- `GET /api/products` - Get all products
- `GET /api/products/<id>` - Get single product
- `POST /api/products` - Create new product
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product

### Shopping Cart
- `GET /api/cart/<user_id>` - Get user's cart
- `POST /api/cart` - Add item to cart
- `PUT /api/cart/<cart_item_id>` - Update cart item quantity
- `DELETE /api/cart/<cart_item_id>` - Remove item from cart
- `POST /api/cart/clear/<user_id>` - Clear user's cart

### Orders
- `POST /api/orders/checkout` - Process checkout and create order
- `GET /api/orders/<user_id>` - Get all orders for a user
- `GET /api/orders/detail/<order_id>` - Get detailed order information

### Authentication
- `POST /api/register` - Register new user

## 🎨 Key Technologies

### Backend
- **Flask**: Web framework
- **MySQL**: Database
- **Flask-CORS**: Cross-origin resource sharing
- **Werkzeug**: Password hashing

### Frontend
- **HTML5**: Markup
- **CSS3**: Styling with modern features (Grid, Flexbox, Animations)
- **JavaScript (ES6+)**: Client-side logic
- **Font Awesome**: Icons

## 📝 Usage Guide

### For Customers

1. **Browse Products**: Visit the shop page to see all available products
2. **Search**: Use the search box to find specific items
3. **Filter**: Select a category to filter products
4. **View Details**: Click the "View" button to see full product information
5. **Add to Cart**: Click "Add to Cart" to add items
6. **Manage Cart**: Visit cart page to update quantities or remove items
7. **Checkout**: Click "Proceed to Checkout" to complete your order
8. **Success Confirmation**: See a beautiful popup confirming your order
9. **View Orders**: Navigate to "My Orders" to see all your order history
10. **Order Details**: Click "View Details" on any order to see complete information

### For Admins

1. **Access Admin Panel**: Navigate to the admin page
2. **Add Product**: Click "Add New Product" button
3. **Edit Product**: Click the edit icon next to any product
4. **Delete Product**: Click the delete icon (with confirmation)
5. **Monitor Stock**: Check stock badges for inventory levels

## 🎯 Features in Detail

### Product Management
- Add unlimited products with images
- Rich product descriptions
- Category organization
- Stock tracking
- Price management

### Shopping Cart
- Add multiple items
- Update quantities on the fly
- Automatic subtotal calculation
- Tax calculation (10%)
- Stock validation

### Order System
- Complete checkout process
- Order creation with detailed items
- Automatic stock reduction
- Order history tracking
- Beautiful success popup
- Detailed order views
- Tax and total calculations
- Order number generation

### UI Enhancements
- Gradient backgrounds
- Card-based layouts
- Smooth hover effects
- Loading spinners
- Toast notifications
- Modal dialogs
- Responsive design
- Mobile-friendly navigation

## 🔧 Configuration

### Default User (for Demo)
The application uses `user_id: 1` for cart operations. In production, integrate with the authentication system.

### Customization
- **Colors**: Edit CSS variables in `style.css` (`:root` section)
- **Product Categories**: Update category dropdowns in HTML files
- **Tax Rate**: Modify calculation in `cart.js`
- **Sample Data**: Edit `seed_products.py` to customize initial products

## 🐛 Troubleshooting

**Database Connection Error**
- Ensure MySQL server is running
- Check credentials in environment variables
- Verify MySQL user has proper permissions

**CORS Errors**
- Make sure Flask-CORS is installed
- Check that backend is running on the correct port

**Products Not Loading**
- Verify backend server is running
- Check browser console for errors
- Ensure API URL in JS files matches backend URL

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Images from Unsplash API
- Icons from Font Awesome
- Inspiration from modern e-commerce platforms

---

**Happy Shopping! 🛒**

For issues or questions, please open an issue in the repository.
