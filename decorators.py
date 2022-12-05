import os
from dotenv import load_dotenv
from functools import wraps

from flask import make_response, jsonify, request

load_dotenv()
USER = os.getenv("API_USER")
PASSWORD = os.getenv("API_PASSWORD")


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        username = request.authorization.username
        password = request.authorization.password
        if not (username and password):
            return make_response(jsonify({"message": "A valid auth data!"}), 401)
        if username != USER or password != PASSWORD:
            return make_response(jsonify({"message": "Invalid username or password!"}), 401)
        return f(*args, **kwargs)
    return decorator
