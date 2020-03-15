# gsheet-fetch
An automation script that fetches data from Google Sheet and imports in an RDBMS

## How to run
* Build docker `docker build -t gsheet-fetch .`
* Run docker `docker run --rm --env-file=.env --name gsheet-fetch gsheet-fetch`

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

## Authentication
This script needs credentials to connect:
* To Google Sheets API and fetch data. For this we use service account, so in order to run you need to 
provide your credentials json. In order to do this you can download the json from Google and then run the following:
```python
import json
with open("credentials.json", "r") as fin:  # Provide the full path of your credentials json
    js = json.load(fin)
with open(".env", "a") as fout:     # Assuming you are in the root of gsheet-fetch project
    fout.write(f"GSHEET_API_SERVICE_ACCOUNT_CREDENTIALS={json.dumps(js)}")
```
* To PostgresDB and push data. For this you need to provide db details for JDBC connection.

For more details on how to set those credentials check [Environment Variables](#environment-variables)

## Environment Variables
This project uses dotenv to easily provide environment variables. The same file can be passed to docker.
Below you can find an example file.
```bash
# Example gsheet-fetch/.env

# Script config
APP_LOGLEVEL=DEBUG 

# Google API 
GSHEET_API_SERVICE_ACCOUNT_CREDENTIALS=...
GSHEET_SPREADSHEET_ID=...
GSHEET_SHEET_DAILY_NAME=Cases
GSHEET_SHEET_LIVE_NAME=Home!A:Z
GSHEET_POLLING_INTERVAL_SEC=10
GSHEET_TIMEOUT_SEC=300

# Postgres JDBC
DB_HOST=localhost
DB_NAME=postgres
DB_USER=user
DB_PASSWORD=123
```
