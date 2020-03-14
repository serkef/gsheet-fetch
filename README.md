# gsheet-fetch
An automation script that fetches data from Google Sheet and imports in an RDBMS

## How to run
* Build docker `docker build -t gsheet-fetch .`
* Run docker `docker run --rm --name gsheet-fetch gsheet-fetch`

## How to develop
* Checkout the repository `git clone git@github.com:COVID2019-app/gsheet-fetch.git`
* Make sure you have python3.8 `python --version`
* Create a virtual environment `python -m venv venv`
* Activate the environment `source venv/bin/activate`
* Install poetry `pip install 'poetry==1.0.5'`
* Install project, along with the extras for development `poetry install`
* Install pre-commit hooks `pre-commit install`

> From now on any commit you make, will go through some basic checks regarding 
formatting.

* Run tests `pytest test`
* To check pre-commit hooks: `pre-commit run`
