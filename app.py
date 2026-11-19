import os
from flask import Flask, send_from_directory, render_template
from flask_login import LoginManager
from config import Config
from models import db, User, Category
from routes import auth_bp, main_bp, api_bp, admin_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(Config.ORIGINALS_FOLDER, exist_ok=True)
    os.makedirs(Config.PROCESSED_FOLDER, exist_ok=True)
    os.makedirs(Config.THUMBNAILS_FOLDER, exist_ok=True)
    os.makedirs(os.path.join(Config.BASE_DIR, 'instance'), exist_ok=True)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    @app.route('/uploads/<path:filename>')
    def serve_uploaded_file(filename):
        return send_from_directory(Config.UPLOAD_FOLDER, filename)

    @app.context_processor
    def inject_global_data():
        return {
            'app_name': 'AI Smart Image Tag Generator',
            'app_version': '2.0.0 Pro'
        }

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template(
            'base.html',
            error_title="404 - Page Not Found",
            error_message="The requested page could not be located."
        ), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template(
            'base.html',
            error_title="403 - Forbidden",
            error_message="You do not have permission to access this resource."
        ), 403

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template(
            'base.html',
            error_title="500 - Internal Server Error",
            error_message="An unexpected system error occurred. Our team has been notified."
        ), 500

    with app.app_context():
        db.create_all()
        seed_categories()

    return app


def seed_categories():
    default_categories = [
        ('Objects', 'bi-box-seam', 'Physical everyday objects, items and tools'),
        ('Animals', 'bi-feather', 'Domestic pets, wild animals, birds and fauna'),
        ('People', 'bi-people', 'Humans, faces, portraits and crowds'),
        ('Vehicles', 'bi-car-front', 'Cars, bikes, trucks, planes and transit'),
        ('Nature & Landscape', 'bi-tree', 'Forests, parks, mountains, waters and skies'),
        ('Food & Drink', 'bi-cup-hot', 'Meals, snacks, beverages and ingredients'),
        ('Architecture & Places', 'bi-buildings', 'Buildings, monuments, interiors and urban scenes'),
        ('Activities & Sports', 'bi-trophy', 'Sports, actions, hobbies and movements'),
        ('Colors & Attributes', 'bi-palette', 'Visual shades, patterns and visual styles'),
        ('General', 'bi-tags', 'General contextual keywords and concepts')
    ]
    try:
        if Category.query.count() == 0:
            for name, icon, desc in default_categories:
                cat = Category(name=name, icon=icon, description=desc)
                db.session.add(cat)
            db.session.commit()
            print("[DATABASE] Seeded default categories successfully.")
    except Exception as e:
        print(f"[DATABASE NOTICE] Category seeding: {e}")


app = create_app()

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 AI SMART IMAGE TAG GENERATOR SERVER STARTING")
    print("=" * 60)
    print("  Local URL:   http://127.0.0.1:5000")
    print("  Models:      YOLOv8 Object Detection + BLIP Captioning")
    print("  Database:   ", app.config.get('SQLALCHEMY_DATABASE_URI'))
    print("=" * 60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)