import os


class Config:
    """Default Flask configuration with MySQL connection settings."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me')
    DEBUG = os.environ.get('FLASK_DEBUG', '1') in ('1', 'true', 'True')

    MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'app_db')
    MYSQL_POOL_NAME = os.environ.get('MYSQL_POOL_NAME', 'app_pool')
    MYSQL_POOL_SIZE = int(os.environ.get('MYSQL_POOL_SIZE', 5))