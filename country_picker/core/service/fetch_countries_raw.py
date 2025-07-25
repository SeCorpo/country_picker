import requests
from typing import List, Dict, Any
from country_picker.core.utils.logger import get_logger

logger = get_logger(__name__)

def fetch_countries_raw() -> List[Dict[str, Any]]:
    """ Returns a list of dicts """
    logger.info('Fetching...')
    url = "https://www.apicountries.com/countries"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list):
        logger.error("Response is not a list as expected.")
        raise ValueError("Response is not a list as expected.")
    logger.info(f"Fetched {len(data)} countries.")
    return data