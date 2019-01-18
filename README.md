# simple-quiz
A simple multiple choice quiz written with a Python3 Django backend and
a ReactJS frontend.

NB: If you do intend on deploying this code to a live environment,
I would highly advise editing back-end/maths/maths/settings.py and
edit the SECRET_KEY to something else. Otherwise bad things may happen.

## Requirements

* Python 3.6+
* NodeJS 10.15.0+
* A database library. By default we are using sqlite3.

An example of a database library, on Ubuntu 18.04, run the command

`sudo apt install libsqlite3-dev`


## Installation

### Backend

In the back-end directory,

`pip3 install -r requirements.txt`

To download the required  Python3 packages.

To set up the database and populate it with initial data, run the
following commands

```
python3 manage.py migrate
python3 manage.py example_quiz
python3 manage.py createsuperuser
```

The `migrate command` setups the database tables.
The `example_quiz` command populates the quiz with initial data

The `createsuperuser` creates your admin account.

### frontend

In the front-end directory, run the command

`npm i .`

To install the required NodeJS libraries.

## How to use

To start the frontend, run `npm start` in the front-end directory

To start the backend, run `python3 manage.py runserver` in back-end/maths/

By default, the frontend runs on `localhost:3000` and the backend
runs on `localhost:8000`

You can login to the quiz system via the frontend.

TODO: the frontend is not yet able to render the quiz questions or submit choices yet.

The URL `localhost:8000/admin` allows you to access the administrator
control panel for the quiz so you can customize quizzes, questions and manage users.

## Testing

To run the tests on the backend, run the command

`python3 manage.py example_quiz`

TODO: Write more unit tests and frontend unit tests

## API Documentation by example

The backend restful endpoints. If marked with "(Unprotected)", a JWT token
is also required in the header setup like so

```
Authorization: JWT <token>
```
Where <token> is your JWT token obtained by `/token-auth`

This token confirms with Django who is sending the request.

### /core/users

POST (Unprotected):


```
{
  "username": "example_user"
  "first_name": "example_name"
  "password": "notmyrealpassword"
}
```

returns

```
{
    "token": "someJWTtoken",
    "username": "example_user",
    "first_name": "example_name"
}
```

### /core/quiz/<id>

GET:

```
{
    "user": user_id,
    "quiz": <id>,
    "user_choices": [
        7,
        5,
        8,
        3
    ],
    "score": 3
}
```

POST:

```
{
	"user_choices": [3,5,7,8]
}
```

returns

```
{
    "success": true,
    "response": {
        "user": 2,
        "quiz": 1,
        "user_choices": [
            7,
            5,
            8,
            3
        ],
        "score": 2
    }
}
```

### /quiz/<id>

GET: returns a list of questions and choices associated with a quiz

```
[
    {
        "id": 1,
        "question_text": "What is 2 + 2?",
        "position": 1,
        "choices": [
            {
                "id": 1,
                "choice_text": "0",
                "position": 1
            },
            {
                "id": 2,
                "choice_text": "5",
                "position": 2
            },
            {
                "id": 3,
                "choice_text": "4",
                "position": 3
            }
        ]
    },
]
```

### /token-auth

POST (Unprotected):

```
{
  "username": "example_user"
  "password": "notmyrealpassword"
}
```

Returns

```
{
    "token": "someJWTtoken",
    "user": {
        "username": "example_user",
        "first_name": "example_name"
    }
}
```

NB if you run `python3 manage.py example_quiz` the pre-populated quiz will be associated with the ID of 1

## TODO
* The frontend is not yet able to render the quiz questions or submit choices yet.
* Write more unit tests for the frontend and backend
* Write more API tests for the backend
* Potentially setup a versioning scheme for the backend API's
* Containerise via docker
