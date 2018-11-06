# Introduction
Vessel is an opinionated bootstrap of files to setup an API centric Flask application.

Its aims to provide a simple set of files and configuration required for building API services using Flask.
Vessel is strongly opinionated about how control flows across your application, but its also very extensible.
You can install any python packages you want and/or remove the ones you do not want.

## Setup
To use Vessel, clone this repo into `project_root`, ensure your python environments are configured and activated. 

Run: `$ pip install -r requirements.txt`

This will pull and install all vessel dependencies into the current or active virtual environment. Copy the content of 
`.env_sample` into `.env` and set proper environment variables.


## Start Server
In the `project_root` with environment activated, 

Run: `$ python run.py runserver`

Open your browser and enter `http://127.0.0.1:5000/api/v1/`

## vessel CLI Tool
Vessel comes with a small CLI tool to help generate commmonly used utilities like `models`, `repositories`, `blueprints`,
 `controllers`, `tests` and `factories`
 
 Example:
 ```
 Usage: python vessel.py
 
 Command Line Arguments
    make:model name eg. python vessel.py make:model user [--with_repo [_controller] ]
	make:repo name eg. python vessel.py make:repo user
	make:blueprint name eg. python vessel.py make:blueprint vendors [--url_prefix=vendors]
	make:controller name eg. python vessel.py make:controller user
	make:test name eg python vessel.py make:test test_user_repo - This command will parse paths and write to the valid paths provided
	make:factory name eg python vessel.py make:factory role
    show_routes eg python vessel.py show_routes
 ```

## Tests
Ofcourse there's support for testing using pytest. To create a new test suite, simply run the make:test command on the CLI. 

eg. `$ python vessel.py make:test integration/endpoints/test_user_endpoints`

To run tests `$ python -m pytest`

## Folder and Code Structure
```
|-- project_root
    |-- app/
        |-- blueprints/
            |-- base_blueprint.py
        |-- controllers/
            |-- __init__.py
            |-- base_controller.py
        |-- models/
            |-- __init__.py
            |-- base_model.py
        |-- repositories/
            |-- __init__.py
            |-- base_repo.py
        |-- utils/
            |-- __init__.py
            |-- auth.py
            |-- security.py
        |-- __init__.py
        |-- test_db.db
    |-- config/
        |-- __init__.py
        |-- env.py
    |-- factories
        |-- __init__.py
    |-- migrations
    |-- tests
        |-- integration/
            |-- endpoints/
                |-- __init__.py
                |-- test_dummy_endpoints.py
            |-- __init__.py
        |-- unit
            |-- repositories/
            |-- test_auth.py
        |-- __init__.py
        |-- base_test_case.py
    |-- .env_sample
    |-- .gitignore
    |-- LICENSE
    |-- Procfile
    |-- pytest.ini
    |-- README.md
    |-- requirements.txt
    |-- run.py
    |-- vessel.py
```
## Procfile
For Heroku enthusiast. Delete if you'd not be deploying to Heroku.

## Bugs, Corrections, Feedback, Contributing
No system is 100% I'd be happy if you can jump in and collaborate. If you find bugs or errors or see places where you can improve on,
fork the repo, and raise a PR or shoot me an email. jcobhams[at]gmail[dot]com