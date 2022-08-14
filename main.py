import logging
from get_files import get_files
from data_processing import data_processing
from create_update_db import create_update_db


def main():
    logging.basicConfig(
        filename="logs.log",
        encoding="utf-8",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)
    logger.info(f"Start the main module")

    get_files()
    tables = data_processing()
    create_update_db(tables)

    logger.info(f"Close the main module")


if __name__ == "__main__":
    main()
