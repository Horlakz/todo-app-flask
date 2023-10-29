from flask import Blueprint, jsonify

from middlewares.authentication import token_required

user_controller = Blueprint("user_controller", __name__)


@user_controller.get("/user")
@token_required
def get_user(user):
    return jsonify(user)
