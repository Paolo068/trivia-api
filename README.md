Endpoints and expected behaviors
GET '/categories'

Retrieves a dictionary of categories in which the keys are the IDs, and the value is the corresponding category string
Query arguments: none
Returns: an object with a single key, categories, which contains an object of id:category_string key:value pairs.
{
'categories': { '1': "Science",
'2': "Art",
'3': "Geography",
'4': "History",
'5': "Entertainment",
'6': "Sports" }
}
GET '/issues?page=${integer}'

Retrieves a paginated set of questions, total number of questions, all categories, and the current category string.
Query arguments: "page" - integer
Returns: an object with 10 paginated questions, the total questions, the object including all categories, and the current category string
{
'Questions': [
{
'id': 1,
'question': 'This is a question',
'response': 'This is a response',
'difficulty': 5,
'category': 2
},
],
'totalQuestions': 100,
'categories': { '1': "Science",
'2': "Art",
'3': "Geography",
'4': "History",
'5': "Entertainment",
'6': "Sports" },
'currentCategory': 'History'
}
GET '/categories/${id}/questions'

Retrieves questions for a category specified by the request id argument
Query arguments: "id" - integer
Returns: an object with questions for the specified category, total questions, and current category string
{
'Questions': [
{
'id': 1,
'question': 'This is a question',
'response': 'This is a response',
'difficulty': 5,
'category': 4
},
],
'totalQuestions': 100,
'currentCategory': 'History'
}
DELETE '/issues/${id}'

Removes a question specified using the question id
Query arguments: "id" - integer
Returns: There is no need to return anything other than the appropriate HTTP status code. It is possible to return the question ID. If you are able to modify the front-end, you can make it delete the question using the id instead of fetching the questions.
POST '/quizzes'

Send a POST request to get the next question
Request body:
{
'previous_questions': [1, 4, 20, 15]
quiz_category': 'current category'
}
Returns: a single new question object
{
'question': {
'id': 1,
'question': 'This is a question',
'response': 'This is a response',
'difficulty': 5,
'category': 4
}
}
POST '/questions'

Send a POST request to add a new question
Request body:
{
'question': 'Here is a new question string',
'response': 'Here is a new response string',
'difficulty': 1,
'category': 3,
}
Returns: does not return new data

POST '/questions/search'

Send a POST request to search for a specific question by search term
Request body:
{
'searchTerm': 'this is the search term'
}

Returns: any array of questions, a number of questions that match the search term and the current category string
{
'Questions': [
{
'id': 1,
'question': 'This is a question',
'response': 'This is a response',
'difficulty': 5,
'category': 5
},
],
'totalQuestions': 100,
'currentCategory': 'Entertainment'
}