from app import app, USERS, models
from flask import request, Response
import json
from http import HTTPStatus
from uuid import uuid1


@app.route("/")
def index():
    return "<h1>Hello World</h1>"


@app.post("/user/create")
def user_create():
    data = request.get_json()
    user_id = str(uuid1())
    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    email = data["email"]

    if not models.User.is_valid_email(email) or not models.User.is_valid_phone(phone):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = models.User(user_id, first_name, last_name, phone, email, score=0)
    USERS[user_id] = user
    # todo: check if user_id already exists
    response = Response(
        # body
        json.dumps(
            {
                "id": user.user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "score": user.score,
            }
        ),
        # status
        HTTPStatus.CREATED,
        # headers
        # content type
        mimetype="application/json",
    )
    return response


@app.get("/user/<string:user_id>")
def get_user(user_id):
    # todo add validation for user_id
    if len(user_id) != 36:
        return Response(status=HTTPStatus.NOT_FOUND)

    user = USERS[user_id]
    response = Response(
        # body
        json.dumps(
            {
                "id": user.user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "score": user.score,
            }
        ),
        # status
        HTTPStatus.CREATED,
        # headers
        # content type
        mimetype="application/json",
    )
    return response
