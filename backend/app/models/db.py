import os
from threading import Lock
from contextlib import contextmanager

import mysql.connector
from mysql.connector import errorcode, pooling
from werkzeug.security import generate_password_hash


MYSQL_SETTINGS = {
    'host': os.environ.get('MYSQL_HOST', '127.0.0.1'),
    'port': int(os.environ.get('MYSQL_PORT', 3306)),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', ''),
}
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'app_db')
POOL_NAME = os.environ.get('MYSQL_POOL_NAME', 'app_pool')
POOL_SIZE = int(os.environ.get('MYSQL_POOL_SIZE', 5))

_pool = None
_pool_lock = Lock()


def ensure_database():
    """Create the target database if it does not already exist."""
    try:
        conn = mysql.connector.connect(**MYSQL_SETTINGS)
    except mysql.connector.Error as exc:
        missing = [k for k, v in MYSQL_SETTINGS.items() if v in (None, '') and k != 'password']
        hint = (
            " Verify your MySQL credentials and environment variables."
            if not missing
            else f" Missing configuration values: {', '.join(missing)}."
        )
        raise RuntimeError(f"Unable to connect to MySQL server.{hint}") from exc
    cursor = conn.cursor()
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DATABASE}` "
        "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
    cursor.close()
    conn.close()


def get_pool():
    """Return a lazily-instantiated MySQL connection pool."""
    global _pool
    if _pool is None:
        with _pool_lock:
            if _pool is None:
                ensure_database()
                config_with_db = {
                    **MYSQL_SETTINGS,
                    'database': MYSQL_DATABASE,
                    'charset': 'utf8mb4',
                    'use_pure': True,
                }
                _pool = pooling.MySQLConnectionPool(
                    pool_name=POOL_NAME,
                    pool_size=POOL_SIZE,
                    autocommit=False,
                    **config_with_db,
                )
                print(
                    f"MySQL connection pool '{POOL_NAME}' ready — "
                    f"{MYSQL_SETTINGS['user']}@{MYSQL_SETTINGS['host']}:{MYSQL_SETTINGS['port']}/{MYSQL_DATABASE}"
                )
    return _pool


@contextmanager
def get_connection():
    """Context manager that yields a pooled connection."""
    pool = get_pool()
    conn = pool.get_connection()
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Ensure required tables exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                phone VARCHAR(32)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                category VARCHAR(100),
                image_url VARCHAR(500),
                stock INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cart_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                product_id INT NOT NULL,
                quantity INT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                UNIQUE KEY unique_user_product (user_id, product_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                total_amount DECIMAL(10, 2) NOT NULL,
                tax_amount DECIMAL(10, 2) NOT NULL,
                grand_total DECIMAL(10, 2) NOT NULL,
                status VARCHAR(50) DEFAULT 'completed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                product_id INT,
                product_name VARCHAR(255) NOT NULL,
                product_price DECIMAL(10, 2) NOT NULL,
                quantity INT NOT NULL,
                subtotal DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        )
        
        conn.commit()


def create_user(username, email, password, phone=None):
    password_hash = generate_password_hash(password)
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO users (username, email, password_hash, phone)
                VALUES (%s, %s, %s, %s)
                """,
                (username, email, password_hash, phone),
            )
            conn.commit()
            user_id = cursor.lastrowid
        except mysql.connector.IntegrityError as exc:
            conn.rollback()
            if exc.errno == errorcode.ER_DUP_ENTRY:
                return None
            raise
    return user_id


def get_user_by_email(email):
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        row = cursor.fetchone()
    return row


# Product functions
def create_product(name, description, price, category, image_url, stock):
    """Create a new product."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO products (name, description, price, category, image_url, stock)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (name, description, price, category, image_url, stock),
        )
        conn.commit()
        return cursor.lastrowid


def get_all_products():
    """Get all products."""
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
        return cursor.fetchall()


def get_product_by_id(product_id):
    """Get a single product by ID."""
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM products WHERE id = %s', (product_id,))
        return cursor.fetchone()


def update_product(product_id, name, description, price, category, image_url, stock):
    """Update an existing product."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE products
            SET name = %s, description = %s, price = %s, category = %s,
                image_url = %s, stock = %s
            WHERE id = %s
            """,
            (name, description, price, category, image_url, stock, product_id),
        )
        conn.commit()
        return cursor.rowcount > 0


def delete_product(product_id):
    """Delete a product."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))
        conn.commit()
        return cursor.rowcount > 0


# Cart functions
def add_to_cart(user_id, product_id, quantity=1):
    """Add or update item in cart."""
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO cart_items (user_id, product_id, quantity)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE quantity = quantity + %s
                """,
                (user_id, product_id, quantity, quantity),
            )
            conn.commit()
            return True
        except mysql.connector.Error:
            conn.rollback()
            return False


def get_cart_items(user_id):
    """Get all cart items for a user with product details."""
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT c.id, c.quantity, p.id as product_id, p.name, p.description,
                   p.price, p.image_url, p.stock,
                   (c.quantity * p.price) as subtotal
            FROM cart_items c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
            ORDER BY c.created_at DESC
            """,
            (user_id,),
        )
        return cursor.fetchall()


def update_cart_quantity(cart_item_id, quantity):
    """Update quantity of a cart item."""
    with get_connection() as conn:
        cursor = conn.cursor()
        if quantity <= 0:
            cursor.execute('DELETE FROM cart_items WHERE id = %s', (cart_item_id,))
        else:
            cursor.execute(
                'UPDATE cart_items SET quantity = %s WHERE id = %s',
                (quantity, cart_item_id),
            )
        conn.commit()
        return cursor.rowcount > 0


def remove_from_cart(cart_item_id):
    """Remove an item from cart."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cart_items WHERE id = %s', (cart_item_id,))
        conn.commit()
        return cursor.rowcount > 0


def clear_cart(user_id):
    """Clear all items from user's cart."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cart_items WHERE user_id = %s', (user_id,))
        conn.commit()
        return True


# Order functions
def create_order(user_id, total_amount, tax_amount, grand_total, cart_items):
    """Create a new order from cart items."""
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            # Create order
            cursor.execute(
                """
                INSERT INTO orders (user_id, total_amount, tax_amount, grand_total)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, total_amount, tax_amount, grand_total),
            )
            order_id = cursor.lastrowid
            
            # Add order items
            for item in cart_items:
                cursor.execute(
                    """
                    INSERT INTO order_items 
                    (order_id, product_id, product_name, product_price, quantity, subtotal)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (order_id, item['product_id'], item['name'], 
                     item['price'], item['quantity'], item['subtotal']),
                )
                
                # Update product stock
                cursor.execute(
                    """
                    UPDATE products 
                    SET stock = stock - %s 
                    WHERE id = %s AND stock >= %s
                    """,
                    (item['quantity'], item['product_id'], item['quantity']),
                )
            
            conn.commit()
            return order_id
        except mysql.connector.Error:
            conn.rollback()
            return None


def get_user_orders(user_id):
    """Get all orders for a user."""
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT * FROM orders 
            WHERE user_id = %s 
            ORDER BY created_at DESC
            """,
            (user_id,),
        )
        return cursor.fetchall()


def get_order_details(order_id):
    """Get order with all items."""
    with get_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get order info
        cursor.execute('SELECT * FROM orders WHERE id = %s', (order_id,))
        order = cursor.fetchone()
        
        if not order:
            return None
        
        # Get order items
        cursor.execute(
            """
            SELECT oi.*, p.image_url
            FROM order_items oi
            LEFT JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
            """,
            (order_id,),
        )
        order['items'] = cursor.fetchall()
        
        return order
