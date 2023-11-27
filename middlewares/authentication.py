import os
from functools import wraps

import jwt
from flask import jsonify, request

from models.user import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        jwt_secret = os.environ.get("JWT_SECRET")
        token = None

        if "Authorization" in request.headers:
            header_value = request.headers.get("Authorization")

            if header_value.split(" ")[0] != "Bearer":
                return jsonify({"message": "token must be a bearer token"}), 400

            token = header_value.split(" ")[1]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, jwt_secret, algorithms="HS256")
            user = User.query.filter_by(id=data["sub"]).first()

        except Exception as e:
            return jsonify({"message": str(e)}), 401

        return f(user, *args, **kwargs)

    return decorated
