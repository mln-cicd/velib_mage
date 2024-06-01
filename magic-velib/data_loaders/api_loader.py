import io
import os
import uuid
import pandas as pd
import requests
import logging
logger = logging.getLogger(__name__)

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    logger.info("Fetching data from API...")
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&timezone=Europe/Paris&rows=2000"
    response = requests.get(url, headers={"accept": "application/json"})
    data = response.json()

    if not os.path.exists(DL_DIR):
        logger.info("Creating directory: %s", DL_DIR)
        os.makedirs(DL_DIR)

    logger.info("Saving data to file: %s", DL_FILE)
    with open(DL_FILE, 'w') as file:
        json.dump(data, file)

    current_md5 = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
    logger.info("Saving MD5 hash to file: %s", MD5_FILE)
    with open(MD5_FILE, 'w') as file:
        file.write(current_md5)

    logger.info("Data fetched and saved successfully.")

    return pd.read_csv(io.StringIO(response.text), sep=',')


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
