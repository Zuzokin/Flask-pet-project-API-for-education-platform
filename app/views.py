from app import app, USERS, EXPRS, QUEST, models
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
    # user_id = str(len(USERS))
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
    if not models.User.is_valid_id(user_id):
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
    # expr_id = str(len(EXPRS))
    count_nums = data["count_nums"]
    operation = data["operation"]  # expected +, *, -, //, **
    if operation == "random":
        operation = random.choice(["+", "-", "*", "//", "**"])
    min_number = data["min"]
    max_number = data["max"]

    if count_nums <= 1 or (count_nums > 2 and operation not in {"+", "*"}):
        return Response(status=http.HTTPStatus.BAD_REQUEST)

    expression = models.Expression(
        expr_id, operation, min_number, max_number, count_nums
    )
    EXPRS[expr_id] = expression

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


@app.get("/math/<string:expr_id>")
def get_expr(expr_id):
    if not models.Expression.is_valid_id(expr_id):
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


@app.post("/math/<string:expr_id>/solve")
def solve_expr(expr_id):
    data = request.get_json()
    user_id = data["user_id"]
    user_answer = data["user_answer"]

    if not models.Expression.is_valid_id(expr_id) or not models.User.is_valid_id(
        user_id
    ):
        return Response(status=HTTPStatus.NOT_FOUND)
    expression = EXPRS[expr_id]
    user = USERS[user_id]

    if user_answer == expression.answer:
        user.increase_score(expression.reward)
        result = "correct"
    else:
        result = "wrong"

    return Response(
        json.dumps(
            {
                "expression_id": expr_id,
                "result": result,
                "reward": expression.reward,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@app.post("/questions/create")
def create_question():
    data = request.get_json()
    title = data["title"]
    description = data["description"]
    question_type = data["type"]
    question_id = str(uuid1())
    # question_id = str(len(EXPRS))
    question = None
    if question_type == "ONE-ANSWER":
        answer = data["answer"]  # expecting string
        if not models.OneAnswer.is_valid(answer):
            return Response(status=HTTPStatus.BAD_REQUEST)
        question = models.OneAnswer(question_id, title, description, answer, reward=1)
    elif question_type == "MULTIPLE-CHOICE":
        choices = data["choices"]  # expecting list
        answer = data["answer"]  # expecting number
        if not models.MultipleChoice.is_valid(answer, choices):
            return Response(status=HTTPStatus.BAD_REQUEST)
        question = models.MultipleChoice(
            question_id, title, description, answer, choices, reward=1
        )

    QUEST[question_id] = question

    return Response(
        json.dumps(
            {
                "id": question.question_id,
                "title": question.title,
                "description": question.description,
                "type": question_type,
                "answer": question.answer,
            }
        ),
        status=HTTPStatus.CREATED,
        mimetype="application/json",
    )
