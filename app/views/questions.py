from app import app, QUEST, USERS, models
from flask import request, Response, url_for
import json
from http import HTTPStatus
from uuid import uuid1
import random


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
            return Response(
                "answer must be string",
                status=HTTPStatus.CREATED,
            )
        question = models.OneAnswer(question_id, title, description, answer, reward=1)
    elif question_type == "MULTIPLE-CHOICE":
        choices = data["choices"]  # expecting list
        answer = data["answer"]  # expecting number
        if not models.MultipleChoice.is_valid(answer, choices):
            return Response(
                "answer must be int, choices must be list. answer < 0 or answer >= len(choices)",
                status=HTTPStatus.BAD_REQUEST,
            )
        question = models.MultipleChoice(
            question_id, title, description, answer, choices, reward=1
        )
    if question is None:
        return Response(
            "Question must be of ONE-ANSWER or MULTIPLE-CHOICE type",
            status=HTTPStatus.BAD_REQUEST,
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


@app.get("/questions/random")
def get_random_question():
    list_of_questions = list(QUEST.values())
    print(list_of_questions)
    if not list_of_questions:
        return Response(
            "No questions in database. "
            f"Please, <a href='{url_for('create_question')}'>add some questions to your database</a>",
            status=HTTPStatus.NOT_FOUND,
        )
    question = random.choice(list_of_questions)
    return Response(
        json.dumps(
            {
                "id": question.question_id,
                "reward": question.reward,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@app.post("/questions/<string:question_id>/solve")
def solve_question(question_id):
    data = request.get_json()
    user_id = data["user_id"]
    user_answer = data["user_answer"]

    if user_id not in USERS.keys():
        return Response(
            "there is no user with this id in the database.",
            status=HTTPStatus.NOT_FOUND,
        )
    if question_id not in QUEST.keys():
        return Response(
            "there is no question with this id in the database.",
            status=HTTPStatus.NOT_FOUND,
        )

    question = QUEST[question_id]
    user = USERS[user_id]

    if isinstance(question, models.MultipleChoice):
        if not isinstance(user_answer, int):
            return Response(
                "ANSWER for Question MULTIPLE-CHOICE must be int",
                status=HTTPStatus.BAD_REQUEST,
            )
    if isinstance(question, models.OneAnswer):
        if not isinstance(user_answer, str):
            return Response(
                "ANSWER Question ONE-ANSWER must be str",
                status=HTTPStatus.BAD_REQUEST,
            )

    if user_answer == question.answer:
        user.increase_score(question.reward)
        result = "correct"
    else:
        result = "wrong"

    return Response(
        json.dumps(
            {
                "question_id": question_id,
                "result": result,
                "reward": question.reward,
            }
        ),
        mimetype="application/json",
        status=HTTPStatus.OK,
    )
