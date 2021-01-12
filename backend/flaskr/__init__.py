import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)

    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins.
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        # Set Access Control
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        """
        Handle GET Request for getting all categories
        """
        categories_query = Category.query.all()
        categories_dict = {}
        for category in categories_query:
            categories_dict[category.id] = category.type

        # abort 404 if there is no category
        if categories_query is None or len(categories_query) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories_dict
        })

    @app.route('/categories', methods=['POST'])
    def create_category():
        """
        Handle POST Request for creating new category
        """
        body = request.get_json()
        type = body.get('type', None)
        try:
            if type is None:
                abort(400)

            category = Category(type=type)
            category.insert()

            categories_query = Category.query.all()
            categories_dict = {}
            for category in categories_query:
                categories_dict[category.id] = category.type

            return jsonify({
                'success': True,
                'categories': categories_dict,
                'total': len(categories_dict)
            })
        except:
            abort(422)

    @app.route('/questions')
    def get_questions():
        """
        Handle GET Request for getting all questions
        """
        # getting paginated questions
        questions = Question.query.all()

        current_questions = paginate_questions(request, questions)

        # getting all categories
        catigories = Category.query.all()
        categories_dict = {}
        for category in catigories:
            categories_dict[category.id] = category.type

        # abort 404 if there is no questions
        if questions is None or len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories_dict,
            'current_category': None,
            'questions': current_questions,
            'total_questions': len(questions)
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        Handle DELETE Request for deleting a question by id
        """
        try:
            question = Question.query.get(question_id)

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question.id
            })
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        '''
        Handle POST Requests for creating new questions and searching questions.
        '''
        body = request.get_json()

        answer = body.get('answer', None)
        category = body.get('category', None)
        question = body.get('question', None)
        difficulty = body.get('difficulty', None)
        search_term = body.get('searchTerm', None)

        if search_term:
            # query the database using search term
            filtered_questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            # 404 if there is no results
            if (len(filtered_questions) == 0):
                abort(404)

            # paginate the results
            current_questions = paginate_questions(request, filtered_questions)
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(filtered_questions)

            })

        # if there is no searchTrem then => create new question
        else:
            try:
                # create and insert new question
                new_question = Question(answer=answer, category=category, question=question, difficulty=difficulty)
                new_question.insert()

                # getting paginated questions
                questions = Question.query.all()
                current_questions = paginate_questions(request, questions)

                return jsonify({
                    'success': True,
                    'created': new_question.id,
                    'questions': current_questions,
                    'total_questions': len(questions)
                })
            except:
                abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        '''
        Handle GET Requests for getting questions based on category.
        '''
        category = Category.query.get(category_id)

        questions = Question.query.join(Category, Question.category == category_id).all()

        current_questions = paginate_questions(request, questions)

        if (category is None):
            abort(400)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'current_category': category.type
        })

    @app.route('/quizzes', methods=['POST'])
    def get_random_quiz_question():
        '''
        Handle POST requests for playing quiz.
        '''
        body = request.get_json()
        previous = body.get('previous_questions', None)
        category = body.get('quiz_category', None)

        if (category is None):
            abort(400)

        previous_questions = []
        if previous:
            previous_questions = previous

        # if catefory == ALL then => return all questions
        if (category['id'] == 0):
            question = Question.query.filter(Question.id.notin_(previous_questions)).first()
        # return questoins for given category
        else:
            question = Question.query.filter(
                Question.category == category['id'], Question.id.notin_(previous_questions)).first()

        return jsonify({
            "success": True,
            "question": question.format() if question != None else None
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(405)
    def not_allawed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allawed"
        }), 405
    return app
