import json
from operator import ne
import os
from this import s
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,PATCH,DELETE,OPTIONS"
        )
        return response

    def paginate_questions(request, questions):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [q.format() for q in questions]
        current_questions = questions[start:end]

        return current_questions

    # --------------------------------------------------------------
    # GET ALL CATEGORIES
    # --------------------------------------------------------------
    @app.route("/categories", methods=["GET"])
    def get_categories():
        try:
            selection = Category.query.order_by(Category.id).all()
            if selection is None:
                abort(404)

            categories = [category.format() for category in selection]

            return jsonify(
                {
                    "success": True,
                    "categories": categories,
                    "total_categories": len(Category.query.all()),
                }
            )
        except:
            abort(400)

    # --------------------------------------------------------------
    # GET ALL QUESTIONS
    # --------------------------------------------------------------
    @app.route("/questions", methods=["GET"])
    def get_questions():
        try:
            categ = Category.query.order_by(Category.id).all()
            selection = Question.query.order_by(Question.id).all()

            if selection is None:
                abort(404)

            questions = paginate_questions(request, selection)
            categories = [cat.format() for cat in categ]

            if len(questions) == 0:
                abort(422)

            return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "categories": categories,
                    "total_questions": len(Question.query.all()),
                }
            )
        except:
            abort(404)

    # --------------------------------------------------------------
    # DELETE QUESTION
    # --------------------------------------------------------------
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_questions(question_id):
        try:
            question = Question.query.filter(
                Question.id == int(question_id)
            ).one_or_none()
            selection = Question.query.all()
            question.delete()

            return jsonify(
                {
                    "success": True,
                    "questions": paginate_questions(request, selection),
                    "deleted": question_id,
                    "total_questions": len(Question.query.all()),
                }
            )

        except:
            abort(404)

    # --------------------------------------------------------------
    # CREATE NEW QUESTION
    # --------------------------------------------------------------
    @app.route("/questions", methods=["POST"])
    def create_or_search_questions():

        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category_type = body.get("category", None)
        new_difficulty = body.get("difficulty", None)
        search_term = body.get("searchTerm", None)


        if search_term:
            selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(search_term))
            )

            questions = [elt.format() for elt in selection]
            if questions:
                return jsonify(
                    {
                        "success": True,
                        "questions": questions,
                        "total_questions": len(Question.query.all()),
                    }
                )
            else:
                abort(404)
        else:
            if (
                new_question
                == new_answer
                == new_difficulty
                == new_category_type
                == None
            ):
                abort(400)

            question = Question(
                question=new_question,
                answer=new_answer,
                difficulty=new_difficulty,
                category=new_category_type,
            )

            question.insert()

            selection = Question.query.order_by(Question.id.desc()).all()
            questions = [elt.format() for elt in selection]
            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": questions,
                    "total_questions": len(Question.query.all()),
                }
            )

    # --------------------------------------------------------------
    # GET QUESTIONS BY CATEGORY
    # --------------------------------------------------------------
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        # body = request.get_json()
        # categ_id = body.get("category")
        if not category_id:
            abort(400)

        if not isinstance(category_id, int):
            abort(400)
        selection = Question.query.filter(Question.category == category_id).all()
        categories = Category.query.all()
        if not selection:
            abort(404)
        questions = paginate_questions(request, selection)
        return jsonify(
            {
                "success": True,
                "questions": questions,
                "categories": [cat.format() for cat in categories],
                "total_questions": len(questions),
            }
        )

    # --------------------------------------------------------------
    # UPDATE QUESTION
    # --------------------------------------------------------------
    @app.route("/questions/<int:question_id>", methods=["PATCH"])
    def update_question(question_id):
        body = request.get_json()

        if question_id:
            if isinstance(question_id, int):
                question = Question.query.filter(
                    Question.id == question_id
                ).one_or_none()

                if question is None:
                    abort(404)

                if "question" in body:
                    question.question = str(body.get("question"))
                elif "answer" in body:
                    question.answer = str(body.get("answer"))
                elif "category" in body:
                    question.category = int(body.get("category"))
                elif "difficulty" in body:
                    question.difficulty = int(body.get("difficulty"))

                question.update()
                return jsonify(
                    {
                        "success": True,
                        "questions": question_id,
                        "total_questions": len(Question.query.all()),
                    }
                )
            else:
                abort(400)
        else:
            abort(422)

    # --------------------------------------------------------------
    # SELECT RANDOM QUESTIONS TO PLAY THE QUIZ
    # --------------------------------------------------------------
    @app.route("/quizzes", methods=["POST"])
    def play_quizz():
        body = request.get_json()

        category = body.get("category", None)
        difficulty = body.get("difficulty", None)

        # Check if the vars exist. If not switch to the next condition
        if category and difficulty:

            # Check if the vars are integer. category and difficulty are foreign keys in Question table referenced by their id
            if isinstance(category, int) and isinstance(difficulty, int):
                selection = Question.query.filter(
                    Question.category == category, Question.difficulty == difficulty
                ).all()

                # Needed to be serializable by the jsonify() function
                questions = [q.format() for q in selection]

                # If corresponding questions found, return JSON or abort
                if questions:
                    return jsonify(
                        {
                            "success": True,
                            "questions": random.choice(questions),
                            "total_questions": len(Question.query.all()),
                        }
                    )
                else:
                    abort(404)
            else:
                abort(400)

        elif category:
            if isinstance(category, int):
                selection = Question.query.filter(Question.category == category).all()
                questions = [q.format() for q in selection]
                if questions:
                    return jsonify(
                        {
                            "success": True,
                            "questions": random.choice(questions),
                            "total_questions": len(Question.query.all()),
                        }
                    )
                else:
                    abort(404)
            else:
                abort(400)

        elif difficulty:
            if isinstance(difficulty, int):
                selection = Question.query.filter(
                    Question.difficulty == difficulty
                ).all()
                questions = [q.format() for q in selection]
                if questions:
                    return jsonify(
                        {
                            "success": True,
                            "questions": random.choice(questions),
                            "total_questions": len(Question.query.all()),
                        }
                    )
                else:
                    abort(404)
            else:
                abort(400)
        else:
            return jsonify(
                {
                    "success": True,
                    "questions": random.choice(
                        [q.format() for q in Question.query.all()]
                    ),
                    "total_questions": len(Question.query.all()),
                }
            )

    # --------------------------------------------------------------
    # ERRORS HANDLERS
    # --------------------------------------------------------------
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {"success": False, "message": "ressource not found", "error": "404"}
            ),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "message": "unprocessable", "error": "422"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "message": "bad request", "error": "400"}),
            400,
        )

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify(
                {"success": False, "message": "method not allowed", "error": "405"}
            ),
            405,
        )

    return app
