import os


class AppConfig:
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "https://localhost:5001").split(",")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dbs/foods.db'
