from datetime import datetime
from json import JSONEncoder
import os

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from config.db import init_db
from controllers.todo import todo_controller
from controllers.auth import auth_controller
from controllers.user import user_controller


class CustomJSONEncoder(JSONEncoder):
    "Add support for serializing timedeltas"

    def default(o):
        if type(o) == datetime.timedelta:
            return str(o)
        if type(o) == datetime.datetime:
            return o.isoformat()
        return super().default(o)


app = Flask(__name__)

cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.json_encoder = CustomJSONEncoder
app.register_blueprint(todo_controller)
app.register_blueprint(auth_controller)
app.register_blueprint(user_controller)

init_db(app)


port = os.environ.get("PORT", 3000)
host = os.environ.get("HOST", "0.0.0.0")
debug = os.environ.get("DEBUG", True)


@app.get("/")
def index():
    return jsonify({"about": "Todo App", "message": "OK"})


if __name__ == "__main__":
    app.run(host=host, port=port, debug=debug == "True")
