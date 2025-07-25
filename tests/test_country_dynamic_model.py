from country_picker.core.service.fetch_countries_dynamic import fetch_countries_dynamic
from pydantic import BaseModel

def test_country_dynamic_model():
    """
    Test that dynamic country models are generated, that at least one country is present,
    and that all objects are valid instances of the same dynamic model, are Pydantic BaseModel instances,
    and have a .name attribute
    """
    country_objs = fetch_countries_dynamic()
    assert country_objs, "No countries returned!"
    country_model = type(country_objs[0])
    assert issubclass(country_model, BaseModel), "Dynamic model is not a subclass of BaseModel"
    for i, obj in enumerate(country_objs):
        assert isinstance(obj, country_model), f"Object {i} is not a country_model"
        assert isinstance(obj, BaseModel), f"Object {i} is not a BaseModel instance"
        assert hasattr(obj, 'name'), f"country_model instance {i} missing .name"
