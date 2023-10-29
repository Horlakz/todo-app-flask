from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv

from config.db import db
from models.user import User

auth_controller = Blueprint("auth_controller", __name__)
load_dotenv()


@auth_controller.post("/register")
def register():
    try:
        data = request.get_json()
        email_exist = User.query.filter_by(email=data["email"]).first()
        username_exist = User.query.filter_by(username=data["username"]).first()
        if email_exist is not None:
            return jsonify({"message": "email already exist"})

        if username_exist:
            return jsonify({"message": "username already exist"})

        hashed_password = generate_password_hash(data["password"], salt_length=10)

        user = User(
            email=data["email"], username=data["username"], password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "user registration is successful"})

    except Exception as e:
        return jsonify({"message": str(e)}), 400


@auth_controller.post("/login")
def login():
    jwt_secret = os.environ.get("JWT_SECRET")
    jwt_expires_in = os.environ.get("JWT_EXPIRES_IN")

    try:
        data = request.get_json()

        if not data.get("username") or not data.get("password"):
            return jsonify({"message": "username and password are required"})

        user = User.query.filter_by(username=data["username"]).first()

        if not user:
            return jsonify({"message": "username does not exist"})

        if not check_password_hash(user.password, data["password"]):
            return jsonify({"message": "password does not match"})

        access_token = jwt.encode(
            {
                "sub": str(user.id),
                "exp": datetime.utcnow() + timedelta(hours=int(jwt_expires_in)),
            },
            jwt_secret,
            algorithm="HS256",
        )

        return jsonify({"token": access_token})

    except Exception as e:
        return jsonify({"message": str(e)}), 400
