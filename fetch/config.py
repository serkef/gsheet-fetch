""" Main configuration and settings """

import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(find_dotenv())

# Script config
RESOURCES = Path(__file__).parent / "resources"
SQL = Path(__file__).parent / "sql"
LOGLEVEL = os.getenv("LOGLEVEL", "INFO")

# Google API
GSHEET_API_SCOPES = os.environ["GSHEET_API_SCOPES"]
GSHEET_API_SERVICE_ACCOUNT_CREDENTIALS = os.environ[
    "GSHEET_API_SERVICE_ACCOUNT_CREDENTIALS"
]
GSHEET_POLLING_INTERVAL_SEC = int(os.getenv("GSHEET_POLLING_INTERVAL_SEC", "60"))
GSHEET_TIMEOUT_SEC = int(os.getenv("GSHEET_POLLING_INTERVAL_SEC", "60"))
GSHEET_SPREADSHEET_ID = os.environ["GSHEET_SPREADSHEET_ID"]
GSHEET_SHEET_DAILY_NAME = os.environ["GSHEET_SHEET_DAILY_NAME"]
GSHEET_SHEET_LIVE_NAME = os.environ["GSHEET_SHEET_LIVE_NAME"]


def read_file(filepath):
    """ Opens a file and returns its content as one string """

    with open(filepath, "r") as fin:
        return fin.read()


# Database
DB_CREATE_RAW_HOME_TABLE = read_file(SQL / "create_raw_home_data.sql")
DB_CREATE_LATEST_HOME_TABLE = read_file(SQL / "create_latest_home_data.sql")
DB_INSERT_RAW_HOME_DATA = read_file(SQL / "insert_raw_home_data.sql")
DB_MIGRATE_DDL = [DB_CREATE_RAW_HOME_TABLE, DB_CREATE_LATEST_HOME_TABLE]


def build_db_session_maker():
    """ Creates an sqlalchemy session for db"""

    # db setup
    connection_string = "postgresql://{user}:{psw}@{host}/{db}".format(
        host=os.getenv("DB_HOST", ""),
        db=os.getenv("DB_NAME", ""),
        user=os.getenv("DB_USER", ""),
        psw=os.getenv("DB_PASSWORD", ""),
    )
    engine = create_engine(connection_string, pool_pre_ping=True)
    session = sessionmaker()
    session.configure(bind=engine)
    return session


DB_SESSION_MAKER = build_db_session_maker()
