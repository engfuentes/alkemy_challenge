import logging
import sqlalchemy as db
import re
from helper import get_current_date
from decouple import config


def create_update_db(tables):
    """Function to create, connect and update the postgres SQL database"""

    logger = logging.getLogger(__name__)
    logger.info(f"Start to update the db")

    # get the environmental variables from .env file
    DATABASE_PASSWORD = config("DATABASE_PASSWORD")
    DATABASE_NAME = config("DATABASE_NAME")

    # Create the database
    engine = db.create_engine(f"postgresql://postgres:Riquelme#10@localhost:5432", echo=True)
    conn = engine.connect()

    conn.execute("commit")
    conn.execute("DROP DATABASE IF EXISTS info_alkemy")
    conn.execute("commit")
    conn.execute("CREATE DATABASE info_alkemy")
    conn.close()

    # Conect to the database
    engine = db.create_engine(f"postgresql://postgres:{DATABASE_PASSWORD}@localhost:5432/{DATABASE_NAME}", echo=True)
    conn = engine.connect()

    # Run the script.sql file that creates the 3 tables in sql
    logger.info(f"Creating tables in sql...")
    with open("script.sql") as file:
        statements = re.split(r";\s*$", file.read(), flags=re.MULTILINE)
        for statement in statements:
            if statement:
                engine.execute(db.text(statement))

    # Update the sql tables with the pandas information
    logger.info(f"Updating tables in sql...")
    _, date_str = get_current_date()

    for i, table in enumerate(tables):
        table["fecha de carga"] = date_str
        table.to_sql(f"table{i+1}", conn, if_exists="replace", index=False)

    conn.close()

    logger.info(f"Finish to update the db")
