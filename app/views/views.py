from app import app, QUEST, EXPRS, USERS
from flask import Response
from http import HTTPStatus


@app.route("/")
def index():
    return Response(
        f"<h3>users:<h3> {'<br>'.join([str(user) for user in USERS.values()])}<br>"
        f"<h3>expressions:<h3> {'<br>'.join([str(expr) for expr in EXPRS.values()])}<br>"
        f"<h3>questions:<h3> {'<br>'.join([str(quest) for quest in QUEST.values()])}<br>",
        status=HTTPStatus.OK,
    )
