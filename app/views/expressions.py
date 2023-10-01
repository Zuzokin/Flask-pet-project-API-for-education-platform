from app import app, USERS, EXPRS, models
from flask import request, Response
import json
from http import HTTPStatus
from uuid import uuid1
import random
import http


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
