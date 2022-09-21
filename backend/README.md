## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return four error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 405: Not Allowed

### Endpoints

#### GET /questions

- Returns a list of question objects, success value, and total number of questions
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Request Arguments: None
- Sample: `curl http://127.0.0.1:5000/questions`

``` json
{
  "questions": [
    {
      "id": 13,
      "question": "What is the largest lake in Africa?",
      "answer": "Lake Victoria",
      "difficulty": 2,
      "category": 3
    },
    {
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?",
      "answer": "The Palace of Versailles",
      "difficulty": 3,
      "category": 3
    },
    {
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?",
      "answer": "Agra",
      "difficulty": 2,
      "category": 3
    },
    {...}
  ],
  "success": true,
  "total_questions": 18
}
```

#### POST /questions

- Creates a new question using the submitted answer, difficulty, question and category. 
- Returns the id of the created question, success value, total questions, and question list based on current page number to update the frontend.
- Can also search for questions if ``search`` term is provided, and returns the corresponding questions
- Request Arguments: None
- `curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" -d '{"answer":"Agra", "question":"The Taj Mahal is located in which Indian city?", "category":"3", difficulty: 2 }'`

```json
{
  "questions": [
    {
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?",
      "answer": "Agra",
      "difficulty": 2,
      "category": 3
    }
    {
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
      "answer": "Tom Cruise",
      "difficulty": 4,
      "category": 5
    },
    {
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
      "answer": "Edward Scissorhands",
      "difficulty": 3,
      "category": 5
    }
  ],
  "created": 15,
  "success": true,
  "total_questions": 17
}
```

#### DELETE /questions/{question_id}

- Deletes the question of the given ID if it exists. 
- Request arguments: ``question_id``
- Returns the id of the deleted question, success value, total questions, and question list based on current page number to update the frontend.
- `curl -X DELETE http://127.0.0.1:5000/questions/16?page=2`

``` json
{
  "questions": [
    {
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
      "answer": "Tom Cruise",
      "difficulty": 4,
      "category": 5
    },
    {
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
      "answer": "Edward Scissorhands",
      "difficulty": 3,
      "category": 5
    },
    {
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?",
      "answer": "Brazil",
      "difficulty": 3,
      "category": 6
    }
  ],
  "deleted": 16,
  "success": true,
  "total_questions": 15
}
```

#### PATCH /questions/{question_id}


- If provided, updates the fields of the specified question. 
- Returns the success value and id of the modified question.
- Request Arguments: ``question_id``
- `curl http://127.0.0.1:5000/questions/15 -X PATCH -H "Content-Type: application/json" -d '{"category":"1"}'`

```json
{
  "id": 15,
  "success": true
}
```
#### POST /quizzes

- Generates one at once a random sets of unique questions
- Filter can be applied based on ``category`` and/or ``difficulty``
- Request Arguments: ``category`` and/or ``difficulty`` but not compulsory
- Returns the success value, the random set of questions and total questions
- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"category": 1, "difficulty": 2}'`

```json
{
  "questions": [
    {
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
      "answer": "Tom Cruise",
      "difficulty": 4,
      "category": 5
    }
  ],
  "success": true,
  "questions": questions,
  "total_questions": 18,
}
```

#### POST /categories

- Retrieve questions based on the category
- Request Arguments: ``category``
- Returns the success value, questions and total questions
- `curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"category": 1}'`

```json
{
  "questions": [
    {
      "id": 1,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
      "answer": "Tom Cruise",
      "difficulty": 4,
      "category": 1
    },
    {
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
      "answer": "Edward Scissorhands",
      "difficulty": 3,
      "category": 1
    },
    {
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?",
      "answer": "Brazil",
      "difficulty": 3,
      "category": 1
    }
  ],
  "success": true,
  "questions": questions,
  "total_questions": 18,
}
```
#### GET /categories

- Retrieve all categories
- Request Arguments: None
- Returns the success value, categories and total categories
- `curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"category": 1}'`

```json
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "success": true,
  "total_categories": 6
}
```
