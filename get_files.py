import logging
import os
import requests
from helper import get_current_date
import sys


def get_files():
    """Function that first creates the required folders and then downloads and saves the 3 csv"""

    logger = logging.getLogger(__name__)
    logger.info(f"Downloading the 3 csv...")

    # Links to the csv
    url_museos = "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museos_datosabiertos.csv"
    url_aulas_cine = "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv"
    url_bibliotecas = "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv"

    # Get the current date in 2 string formats
    year_month_str, date_str = get_current_date()

    cat_dict = {"museos": url_museos, "salas_cine": url_aulas_cine, "bibliotecas": url_bibliotecas}

    for cat, url in cat_dict.items():

        # Create folders if they do not exist
        path = f"./{cat}/{year_month_str}/".lower()
        if not os.path.exists(path):
            logger.info("Creating folders...")
            os.makedirs(path)

        # Request the csv and save it with the corresponding name format
        logger.info(f"Request csv of {cat}")
        try:
            r = requests.get(url)
        except:
            logging.error(f"Error when downloading {cat}.csv. Check the url")
            sys.exit()

        with open(f"./{cat}/{year_month_str}/{cat}-{date_str}.csv", "wb") as f:
            f.write(r.content)
            logger.info(f"csv file of {cat} has been downloaded and saved")

    logger.info(f"Downloading the 3 csv finished")
