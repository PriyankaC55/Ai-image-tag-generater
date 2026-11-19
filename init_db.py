import os
import sys
from app import create_app, db
from models import User, Category


def init():
    app = create_app()
    with app.app_context():
        print(f"Connecting to database: {app.config['SQLALCHEMY_DATABASE_URI']}")
        db.create_all()
        print("✓ All tables verified and created successfully.")

        if User.query.count() == 0:
            admin = User(
                username='admin',
                email='admin@visionai.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Created initial demo administrator: username='admin', password='admin123'")
        else:
            print(f"✓ Found {User.query.count()} existing registered user(s).")

        print(f"✓ Categories count: {Category.query.count()}")
        print("\nDatabase initialization complete! You can now run 'python app.py'.")


if __name__ == '__main__':
    init()