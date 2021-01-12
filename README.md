# Full Stack API Final Project

## Full Stack Trivia

This project is a game where users can test their knowledge answering trivia questions. The task for the project was to create an API and test suite for implementing the following functionality:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

# Getting Started

## Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.

### Backend

From the backend folder run `pip install -r requirements.txt.` All required packages are included in the requirements file.

To run the application run the following commands:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

### Frontend

From the frontend folder, run the following commands to start the client:

```bash
npm install // only once to install dependencies
npm start
```

By default, the frontend will run on localhost:3000.

## Tests

In order to run tests navigate to the backend folder and run the following commands:

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

# API Reference

## Getting Start

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend

- Authentication: This version of the application does not require authentication or API keys.

## Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return three types of errors:

- 400 – Bad Request
- 404 – Not Found
- 405 - Method Not Allawed
- 422 – Unprocessable

## Endpoints

### GET /categories

- General:
  - Returns a list categories.
- Sample: `curl http://127.0.0.1:5000/categories`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

### GET /questions

- General:
  - Returns a list of questions objects, list of categories, current_category, success value, and total number of questions
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/questions`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    ...
  ],
  "success": true,
  "total_questions": 18
}
```

### DELETE /questions/{question_id}

- General:
  - Deletes the question of the given ID if it exists. Returns the id of the deleted question and success value
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/12`

```
{
  "deleted": 12,
  "success": true
}
```

### POST /questions/

- General: This endpoint either creates a new question or returns search results.

  - Searches for questions using search term in JSON request parameters.
    - Returns JSON object with paginated matching questions.
  - Creates a new qurstion using the submitted question, answer, difficulty and category.
    - Returns the id of the created question, success value, total questions, and questions list based on current page number to update the frontend.

- sample `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type:application/json" -d "{\"searchTerm\":\"which\"}"`

```
{
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    ...
  ],
  "success": true,
  "total_questions": 7
}
```

- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type:application/json" -d "{\"question\":\"Who are you?\", \"answer\":\"Elsayed\", \"difficulty\":\"1\", \"category\":\"1\"}"`

```
{
  "created": 60,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    ...
  ],
  "success": true,
  "total_questions": 18
}
```

### GET /categories/{category_id}/questions

- General:

  - Returns a list of questions objects, current category, success value, and total number of questions
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

```
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Elsayed",
      "category": 1,
      "difficulty": 1,
      "id": 60,
      "question": "Who are you?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

### POST /quizzes

- General:

  - Returns a distinct questions objects and success value

- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type:application/json" -d "{\"previous_questions\": [20, 21], \"quiz_category\": {\"type\": \"Science\", \"id\": \"1\"}}"`

```
{
  "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true
}
```

# Authors

Elsayed Ahmed authored the API (`__init__.py`), test suite (test_flaskr.py), and this README.
All other project files, including the models and frontend, were created by [Udacity](https://www.udacity.com/)
