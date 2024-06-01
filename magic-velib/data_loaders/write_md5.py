import hashlib
import json
import os
import logging
from mage_ai.data_preparation.decorators import data_loader

logger = logging.getLogger(__name__)

@data_loader
def write_md5(data, *args, **kwargs):
    logger.info("Writing MD5 hash to file...")
    DL_DIR = '/tmp'
    MD5_FILE = os.path.join(DL_DIR, 'data.md5')

    if not os.path.exists(DL_DIR):
        logger.info("Creating directory: %s", DL_DIR)
        os.makedirs(DL_DIR)

    try:
        current_md5 = hashlib.md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
        with open(MD5_FILE, 'w') as file:
            file.write(current_md5)
        logger.info("MD5 hash written to file successfully.")
        return {'md5_file': MD5_FILE, 'current_md5': current_md5}
    except Exception as e:
        logger.error("Failed to write MD5 hash to file: %s", e)
        raise