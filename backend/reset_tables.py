"""
Script to reset database tables for order system.
Run this if you get database errors after updating the schema.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.models import db

def reset_order_tables():
    """Drop and recreate order-related tables."""
    print("🔧 Resetting order tables...")
    
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Drop tables in correct order (handle foreign keys)
            print("Dropping old tables...")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("DROP TABLE IF EXISTS order_items")
            cursor.execute("DROP TABLE IF EXISTS orders")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            conn.commit()
            print("✓ Old tables dropped")
            
            # Recreate tables
            print("Creating new tables...")
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
            print("✓ Orders table created")
            
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
            print("✓ Order items table created")
            
            conn.commit()
            
        print("\n✅ Tables reset successfully!")
        print("🚀 Now restart your backend server: python run.py")
        
    except Exception as e:
        print(f"\n❌ Error resetting tables: {e}")
        print("\nIf MySQL is not running:")
        print("1. Start MySQL server")
        print("2. Run this script again")
        sys.exit(1)


if __name__ == '__main__':
    print("=" * 60)
    print("DATABASE TABLE RESET UTILITY")
    print("=" * 60)
    print("\nThis will drop and recreate order tables.")
    print("⚠️  WARNING: All existing order data will be lost!")
    print()
    
    response = input("Continue? (yes/no): ").lower().strip()
    
    if response in ('yes', 'y'):
        reset_order_tables()
    else:
        print("❌ Cancelled")

