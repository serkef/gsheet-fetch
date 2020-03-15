""" Main module for gsheet fetch script """
import logging
from time import sleep

from fetch.config import (
    DB_MIGRATE_DDL,
    DB_SESSION_MAKER,
    GSHEET_POLLING_INTERVAL_SEC,
    LOGLEVEL,
)
from fetch.fetchers import HomeData
from fetch.utilities import set_logging


def main():
    """ Runs the main loop for all fetchers """

    set_logging(LOGLEVEL)
    logger = logging.getLogger(f"fetch.fetch:main")

    # Migrate SQL DB
    logger.info(f"Migrating db...")
    cursor = DB_SESSION_MAKER()
    for ddl in DB_MIGRATE_DDL:
        cursor.execute(ddl)
    cursor.commit()
    cursor.close()

    # Initialize Fetchers
    logger.info(f"Initializing Home data fetcher...")
    home_fetcher = HomeData()

    logger.info(f"Starting loop...")
    while True:
        home_fetcher.store()

        logger.debug(f"Waiting {GSHEET_POLLING_INTERVAL_SEC} sec before polling gsheet")
        sleep(GSHEET_POLLING_INTERVAL_SEC)


if __name__ == "__main__":
    main()
