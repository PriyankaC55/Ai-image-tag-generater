import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    BASE_DIR = BASE_DIR

    SECRET_KEY = os.getenv('SECRET_KEY', 'ai-image-smart-tagger-super-secret-key-2026')

    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ORIGINALS_FOLDER = os.path.join(UPLOAD_FOLDER, 'originals')
    PROCESSED_FOLDER = os.path.join(UPLOAD_FOLDER, 'processed')
    THUMBNAILS_FOLDER = os.path.join(UPLOAD_FOLDER, 'thumbnails')
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024

    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
    MYSQL_DB = os.getenv('MYSQL_DB', 'ai_image_tagger')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def get_database_uri(cls):
        custom_url = os.getenv('DATABASE_URL')
        if custom_url:
            return custom_url

        try:
            conn = pymysql.connect(
                host=cls.MYSQL_HOST,
                port=cls.MYSQL_PORT,
                user=cls.MYSQL_USER,
                password=cls.MYSQL_PASSWORD,
                connect_timeout=2
            )

            with conn.cursor() as cursor:
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS `{cls.MYSQL_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
                )
            conn.commit()
            conn.close()

            print(f"[DATABASE] Connected to MySQL database '{cls.MYSQL_DB}' successfully.")

            return f"mysql+pymysql://{cls.MYSQL_USER}:{cls.MYSQL_PASSWORD}@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DB}?charset=utf8mb4"

        except Exception as e:
            print(f"[DATABASE WARNING] Could not connect to MySQL ({e}).")
            print("[DATABASE] Falling back to SQLite database for instant out-of-the-box readiness.")
            sqlite_path = os.path.join(BASE_DIR, 'instance', 'ai_image_tagger.db')
            return f"sqlite:///{sqlite_path}"

    SQLALCHEMY_DATABASE_URI = None


Config.SQLALCHEMY_DATABASE_URI = Config.get_database_uri()