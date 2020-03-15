""" fetchers module containing all Fetcher classes"""
import json
import logging
import socket
from tempfile import NamedTemporaryFile

import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from fetch.config import (
    DB_INSERT_RAW_HOME_DATA,
    DB_SESSION_MAKER,
    GSHEET_API_SERVICE_ACCOUNT_CREDENTIALS,
    GSHEET_SHEET_LIVE_NAME,
    GSHEET_SPREADSHEET_ID,
    GSHEET_TIMEOUT_SEC,
)

socket.setdefaulttimeout(GSHEET_TIMEOUT_SEC)


class GsheetFetcher:
    """ A generic fetcher for Google sheets. Knows how to auth and fetch. """

    def __init__(self, spreadsheet_id, spreadsheet_range, scopes=None):
        self.scopes = scopes or ["https://www.googleapis.com/auth/spreadsheets"]
        self.api = self.get_gsheet_api()
        self.spreadsheet_id = spreadsheet_id
        self.spreadsheet_range = spreadsheet_range
        self.db = DB_SESSION_MAKER().bind

    def get_gsheet_api(self):
        """ Initializes Google API using service account """
        with NamedTemporaryFile("w", delete=False) as tmp:
            json.dump(json.loads(GSHEET_API_SERVICE_ACCOUNT_CREDENTIALS), tmp)
            cred = tmp.name
        credentials = service_account.Credentials.from_service_account_file(
            filename=cred, scopes=self.scopes
        )

        service = build("sheets", "v4", credentials=credentials, cache_discovery=False)
        return service.spreadsheets()  # pylint: disable=E1101

    def fetch(self):
        """ Fetches data from gsheet """

        logger = logging.getLogger("GsheetFetcher.fetch")
        logger.debug("Fetching data...")
        try:
            return (
                self.api.values()
                .get(spreadsheetId=self.spreadsheet_id, range=self.spreadsheet_range)
                .execute()
            )
        except (HttpError, socket.timeout):
            logger.error("Cannot fetch values.", exc_info=True)
            return None


class HomeData(GsheetFetcher):
    """ A Google Sheet fetcher for "Home" sheet """

    def __init__(self):
        super().__init__(
            spreadsheet_id=GSHEET_SPREADSHEET_ID,
            spreadsheet_range=GSHEET_SHEET_LIVE_NAME,
        )

    def process(self):
        """ Fetches and processes gsheet data. Returns a well structured data frame """

        logger = logging.getLogger("HomeData.process")
        data = self.fetch()
        if data is None:
            logger.debug("Fetched no data")
            return None
        logger.info("Processing fetched data...")
        df = pd.DataFrame(data["values"]).iloc[3:, [2, 4, 8, 13, 17, 21, 24]]
        df = df.replace(r"^\s*$", "0", regex=True).fillna(0).reset_index(drop=True)
        df = df.drop(df[df[df.columns[0]].replace("0", pd.NaT).isnull()].index)
        val_cols = ["cases", "deaths", "recovered", "severe", "tested", "active"]
        df.columns = ["rec_territory"] + val_cols
        for field in val_cols:
            df[field] = pd.to_numeric(
                df[field].fillna("0").str.replace(",", ""), errors="coerce"
            )
            df[field] = pd.to_numeric(df[field].fillna("0"))
        return df

    def store(self):
        """ Stores data to db """

        logger = logging.getLogger("HomeData.store")
        df = self.process()
        if df is None:
            return
        logger.debug(f"Fetched {df.shape} dataset")
        logger.info("Storing processed data...")

        df.to_sql("latest_home_data", self.db, if_exists="replace", index=False)
        self.db.execute(
            DB_INSERT_RAW_HOME_DATA,
            [
                (
                    rec.rec_territory,
                    rec.cases,
                    rec.deaths,
                    rec.recovered,
                    rec.severe,
                    rec.tested,
                    rec.active,
                )
                for _, rec in df.iterrows()
            ],
        )
