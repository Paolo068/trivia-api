import json
import os
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

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,PATCH,DELETE,OPTIONS"
        )
        return response

    def paginate_question(request, questions):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        selection = [q.format() for q in questions]
        current_questions = selection[start:end]

        return current_questions

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/categories", methods=["GET"])
    def get_categories():
        try:
            selection = Category.query.order_by(Category.id).all()
            if selection is None:
                abort(404)

            categories = [category.format() for category in selection]
            # for category in selection:
            #     categories = [category.format()]
            return jsonify(
                {
                    "success": True,
                    "categories": categories,
                    "total_categories": len(Category.query.all()),
                }
            )
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/questions", methods=["GET"])
    def get_questions():
        try:
            categ = Category.query.order_by(Category.id).all()
            selection = Question.query.order_by(Question.id).all()

            if selection is None:
                abort(404)

            questions = paginate_question(request, selection)
            categories = [cat.format() for cat in categ]
            # for category in selection:
            #     categories = [category.format()]
            return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "categories": categories,
                    "total_questions": len(Question.query.all()),
                }
            )
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<int:q_id>", methods=["DELETE"])
    def delete_questions(q_id):
        try:
            question = Question.query.filter(Question.id == q_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()

            return jsonify(
                {
                    "success": True,
                    "deleted": q_id,
                    "total_questions": len(Question.query.all()),
                }
            )

        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route("/questions", methods=["POST"])
    def create_questions():
        try:
            body = request.get_json()

            new_question = str(body.get("question"))
            new_answer = str(body.get("answer"))
            new_category_type = int(body.get("category"))
            new_difficulty = int(body.get("difficulty"))

            question = Question(
                question=new_question,
                answer=new_answer,
                difficulty=new_difficulty,
                category=new_category_type,
            )

            question.insert()

            selection = Question.query.order_by(Question.id).all()
            questions = [elt.format() for elt in selection]
            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": questions,
                    "total_questions": len(Question.query.all()),
                }
            )
        except:
            abort(400)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        body = request.get_json()
        search_term = body.get("search", None)
        try:
            if search_term:
                selection = Question.query.order_by(Question.id).where(
                    Question.question.like("%{}%".format(search_term))
                )

                questions = [elt.format() for elt in selection]

                return jsonify(
                    {
                        "success": True,
                        "questions": questions,
                        "total_questions": len(Question.query.all()),
                    }
                )
        except:
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/categories/<int:categ_id>/questions", methods=["GET"])
    def get_questions_by_category(categ_id):

        try:
            if categ_id:
                selection = Question.query.filter(Question.category == categ_id).all()
                categories = Category.query.all()
                formatted_categories = [cat.format() for cat in categories]
                questions = [question.format() for question in selection]
                return jsonify(
                    {
                        "success": True,
                        "questions": questions,
                        "categories": formatted_categories,
                        "total_questions": len(Question.query.all()),
                    }
                )
            else:
                return print("You must provide a valid category id")

        except:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/quizzes", methods=["POST"])
    def get_questions_to_play_quizz():
        # try:
        body = request.get_json()
        category = body.get("category", None)

        if category:
            selection = Question.query.filter(Question.category == category).all()

        else:
            abort(422)

        questions = [elt.format() for elt in selection]

        return jsonify(
            {
                "success": True,
                "questions": [random.choice(questions)],
                "total_questions": len(Question.query.all()),
            }
        )

    # except:
    #     abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
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