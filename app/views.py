from app import app, USERS, EXPRS, models
from flask import request, Response
import json
from http import HTTPStatus
from uuid import uuid1
import random
import http


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

    response = Response(
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
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response


@app.get("/user/<string:user_id>")
def get_user(user_id):
    if user_id not in USERS.keys():
        return Response(status=HTTPStatus.NOT_FOUND)

    user = USERS[user_id]
    response = Response(
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
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/math/expression")
def generate_expr():
    data = request.get_json()
    expr_id = str(uuid1())
    count_nums = data["count_nums"]
    operation = data["operation"]  # expected +, *, -, //, **
    if operation == "random":
        operation = random.choice(["+", "-", "*", "//", "**"])
    min_number = data["min"]
    max_number = data["max"]

    if count_nums <= 1 or (count_nums > 2 and operation not in {"+", "*"}):
        return Response(status=http.HTTPStatus.BAD_REQUEST)

    values = [random.randint(min_number, max_number) for _ in range(count_nums)]
    expression = models.Expression(expr_id, operation, *values)
    EXPRS[expr_id] = expression

    response = Response(
        json.dumps(
            {
                "id": expression.expr_id,
                "operation": expression.operation,
                "values": values,
                "string_expr": expression.to_string(),
                "answer": expression.answer,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/math/<string:expr_id>")
def get_expr(expr_id):
    if expr_id not in EXPRS.keys():
        return Response(status=HTTPStatus.NOT_FOUND)

    expression = EXPRS[expr_id]

    response = Response(
        json.dumps(
            {
                "id": expression.expr_id,
                "operation": expression.operation,
                "values": expression.values,
                "string_expr": expression.to_string(),
                "answer": expression.answer,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response
