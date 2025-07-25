from typing import List
from pydantic import BaseModel
from country_picker.core.service.fetch_countries_raw import fetch_countries_raw
from country_picker.core.utils.dynamic_schema_from_response import dynamic_model_from_response

def fetch_countries_dynamic(model_name: str = "Country") -> List[BaseModel]:
    """
    Fetches all countries, dynamically generates a Pydantic model to match all fields and nested structures
    found in the data, and returns a validated model instance for each country.
    """
    countries = fetch_countries_raw()
    generated_model = dynamic_model_from_response(countries, model_name=model_name)
    return [generated_model.model_validate(c) for c in countries]
