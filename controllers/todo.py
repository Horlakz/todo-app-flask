from sqlalchemy.orm import joinedload
from flask import Blueprint, jsonify, request

from config.db import db
from models.todo import Todo
from middlewares.authentication import token_required

todo_controller = Blueprint("todo_controller", __name__)


@todo_controller.route("/todos", methods=["GET"])
@token_required
def index(user):
    try:
        todos = (
            Todo.query.options(joinedload(Todo.user)).filter_by(user_id=user.id).all()
        )

        return jsonify(todos)
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@todo_controller.route("/todos", methods=["POST"])
@token_required
def create(user):
    try:
        data = request.get_json()

        if not data.get("title"):
            return jsonify({"message": "Title is required!"}), 400

        todo = Todo(title=data["title"], user_id=user.id)
        db.session.add(todo)
        db.session.commit()
        return jsonify({"message": "Todo created", "todo_id": todo.id}), 201
    except Exception as e:
        return jsonify({"message": "Token is invalid!"}), 400


@todo_controller.route("/todos/<todo_id>", methods=["PUT"])
@token_required
def update(user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()
    if not todo:
        return jsonify({"message": "Todo not found"}), 404

    data = request.get_json()

    if data.get("title"):
        todo.title = data["title"]
    if data.get("completed") is not None:
        todo.completed = data["completed"]

    db.session.commit()
    return jsonify({"message": "Todo updated"})


@todo_controller.route("/todos/<todo_id>", methods=["DELETE"])
@token_required
def delete(user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()
    if not todo:
        return jsonify({"message": "Todo not found"}), 404

    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Todo deleted"})
