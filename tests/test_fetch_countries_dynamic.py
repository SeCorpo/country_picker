import random
import pytest
from country_picker.core.service.fetch_countries_dynamic import fetch_countries_dynamic
from pydantic import BaseModel

countries = fetch_countries_dynamic()

def test_countries_is_list():
    assert isinstance(countries, list), "fetch_countries_dynamic() should return a list"


def test_countries_not_empty():
    assert len(countries) > 0, "The list should not be empty"


@pytest.mark.dependency()
def test_all_countries_are_pydantic_models():
    for i, country in enumerate(countries):
        assert isinstance(country, BaseModel), f"Country at index {i} is not a Pydantic BaseModel"


@pytest.mark.dependency(depends=["test_all_countries_are_pydantic_models"])
def test_all_countries_have_name_attr():
    for i, country in enumerate(countries):
        assert hasattr(country, "name"), f"Attribute 'name' missing in country model at index {i}"


@pytest.mark.dependency(depends=["test_all_countries_are_pydantic_models"])
def test_all_countries_have_alpha2code_attr():
    for i, country in enumerate(countries):
        assert hasattr(country, "alpha2Code"), f"Attribute 'alpha2Code' missing in country model at index {i}"


@pytest.mark.dependency(depends=["test_all_countries_are_pydantic_models"])
def test_all_countries_have_region_attr():
    for i, country in enumerate(countries):
        assert hasattr(country, "region"), f"Attribute 'region' missing in country model at index {i}"


@pytest.mark.dependency(depends=["test_all_countries_are_pydantic_models"])
def test_print_first_random_last_country_names():
    first_name = getattr(countries[0], "name", None)
    last_name = getattr(countries[-1], "name", None)
    random_index = random.randint(0, len(countries) - 1)
    random_name = getattr(countries[random_index], "name", None)
    print(f"\nFirst country name: {first_name}")
    print(f"Random country name: {random_name}")
    print(f"Last country name: {last_name}\n")
