"""
Sample script to populate the database with initial product data.
Run this script to add some sample products for testing.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.models import db

# Sample products data
SAMPLE_PRODUCTS = [
    {
        'name': 'Ballpoint Pen Set (10 Pack)',
        'description': 'High-quality ballpoint pens with smooth ink flow. Perfect for everyday writing tasks, exams, and note-taking.',
        'price': 12.99,
        'category': 'Writing Instruments',
        'image_url': 'https://images.unsplash.com/photo-1586951404587-1356a7f285f7?w=400',
        'stock': 50
    },
    {
        'name': 'Mechanical Pencil Set',
        'description': '0.7mm mechanical pencils with ergonomic grip. Includes extra lead refills and erasers.',
        'price': 15.99,
        'category': 'Writing Instruments',
        'image_url': 'https://images.unsplash.com/photo-1606040450952-48b6b3dc831e?w=400',
        'stock': 35
    },
    {
        'name': 'Highlighter Set (6 Colors)',
        'description': 'Vibrant highlighters in assorted colors. Chisel tip for both broad and narrow lines.',
        'price': 8.99,
        'category': 'Writing Instruments',
        'image_url': 'https://images.unsplash.com/photo-1615835818812-e4c4ac0af0e0?w=400',
        'stock': 45
    },
    {
        'name': 'Spiral Notebook (3 Pack)',
        'description': 'College-ruled spiral notebooks with 100 sheets each. Durable covers in various colors.',
        'price': 9.99,
        'category': 'Notebooks',
        'image_url': 'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400',
        'stock': 60
    },
    {
        'name': 'Composition Notebook',
        'description': 'Classic marble composition notebook with 200 pages. Ideal for journaling and note-taking.',
        'price': 5.99,
        'category': 'Notebooks',
        'image_url': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400',
        'stock': 40
    },
    {
        'name': 'Sticky Notes Multi-Pack',
        'description': 'Assorted sizes of sticky notes in bright colors. Great for reminders and quick notes.',
        'price': 7.49,
        'category': 'Notebooks',
        'image_url': 'https://images.unsplash.com/photo-1586075010923-2dd4570fb338?w=400',
        'stock': 55
    },
    {
        'name': 'Geometry Set',
        'description': 'Complete geometry set with compass, protractor, ruler, and triangles in a protective case.',
        'price': 11.99,
        'category': 'School Supplies',
        'image_url': 'https://images.unsplash.com/photo-1596495577886-d920f1fb7238?w=400',
        'stock': 25
    },
    {
        'name': 'Eraser Pack (5 Pieces)',
        'description': 'Premium quality erasers that remove pencil marks cleanly without smudging.',
        'price': 4.99,
        'category': 'School Supplies',
        'image_url': 'https://images.unsplash.com/photo-1589942010411-8118408c5e4d?w=400',
        'stock': 70
    },
    {
        'name': 'Scissors - Stainless Steel',
        'description': 'Professional-grade scissors with comfortable grip handles. Sharp stainless steel blades.',
        'price': 6.99,
        'category': 'School Supplies',
        'image_url': 'https://images.unsplash.com/photo-1589941013453-ec89f33b5e95?w=400',
        'stock': 30
    },
    {
        'name': 'Glue Sticks (12 Pack)',
        'description': 'Non-toxic glue sticks that dry clear. Perfect for school projects and crafts.',
        'price': 8.49,
        'category': 'School Supplies',
        'image_url': 'https://images.unsplash.com/photo-1611532736579-6b16e2b50449?w=400',
        'stock': 50
    },
    {
        'name': 'Colored Pencil Set (24 Colors)',
        'description': 'Vibrant colored pencils with soft cores for smooth coloring. Pre-sharpened and ready to use.',
        'price': 13.99,
        'category': 'Art Supplies',
        'image_url': 'https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=400',
        'stock': 40
    },
    {
        'name': 'Acrylic Paint Set',
        'description': '12-color acrylic paint set with excellent coverage. Suitable for canvas, wood, and paper.',
        'price': 18.99,
        'category': 'Art Supplies',
        'image_url': 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=400',
        'stock': 20
    },
    {
        'name': 'Sketchbook - Premium',
        'description': '100-page sketchbook with heavyweight paper. Perfect for pencil, charcoal, and light markers.',
        'price': 14.99,
        'category': 'Art Supplies',
        'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400',
        'stock': 35
    },
    {
        'name': 'Watercolor Set',
        'description': '36-color watercolor paint set with brush included. Non-toxic and easy to clean.',
        'price': 16.99,
        'category': 'Art Supplies',
        'image_url': 'https://images.unsplash.com/photo-1583241800882-c17c93e4e1e3?w=400',
        'stock': 25
    },
    {
        'name': 'Index Cards (500 Count)',
        'description': 'Ruled index cards for studying, flashcards, and organization. Perforated for easy separation.',
        'price': 6.49,
        'category': 'Notebooks',
        'image_url': 'https://images.unsplash.com/photo-1589998059171-988d887df646?w=400',
        'stock': 45
    }
]


def seed_products():
    """Add sample products to the database."""
    print("🌱 Seeding database with sample products...")
    
    try:
        # Ensure database is initialized
        db.init_db()
        
        # Add each product
        for product_data in SAMPLE_PRODUCTS:
            product_id = db.create_product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                category=product_data['category'],
                image_url=product_data['image_url'],
                stock=product_data['stock']
            )
            print(f"✓ Added: {product_data['name']} (ID: {product_id})")
        
        print(f"\n✅ Successfully added {len(SAMPLE_PRODUCTS)} products to the database!")
        print("🚀 You can now start the server and browse products at http://127.0.0.1:5000")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        sys.exit(1)


if __name__ == '__main__':
    seed_products()

