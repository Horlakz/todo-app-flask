import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app: Flask):
    db_user = os.environ.get("DATABASE_USER")
    db_password = os.environ.get("DATABASE_PASSWORD")
    db_name = os.environ.get("DATABASE_NAME")
    db_host = os.environ.get("DATABASE_HOST")
    db_port = os.environ.get("DATABASE_PORT")
    db_sslmode = os.environ.get("DATABASE_SSLMODE", "require")


    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode={db_sslmode}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
