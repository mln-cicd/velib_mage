
from utils.database.database import get_db_session
from utils.database.models import Location


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import logging
logger = logging.getLogger(__name__)


@transformer
def check_station_codes_count(data, *args, **kwargs):
    session = get_db_session()()
    location_count = session.query(Location).count()
    if location_count > 1450:
        logger.info("Locations table has been successfully populated with 1450+ rows.")
    else:
        logger.info("Failed to populate the locations table with 1450+ rows.")
    return location_count



@test
def test_output(data) -> None:
    """
    Template code for testing the output of the block.
    """
    assert data is not None, 'The output is undefined'
