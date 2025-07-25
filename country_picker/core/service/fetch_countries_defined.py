from typing import List
from country_picker.core.service.fetch_countries_raw import fetch_countries_raw
from country_picker.core.models.country import Country

def fetch_countries_defined() -> List[Country]:
    """ Fetches countries and returns a list of Country model instances using the defined model """
    countries = fetch_countries_raw()
    return [Country.model_validate(c) for c in countries]
