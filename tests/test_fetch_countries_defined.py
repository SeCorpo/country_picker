import random
import pytest
from country_picker.core.service.fetch_countries_defined import fetch_countries_defined
from country_picker.core.models.country import Country

countries = fetch_countries_defined()

def test_countries_is_list():
    assert isinstance(countries, list), "fetch_countries_defined() should return a list"


def test_countries_not_empty():
    assert len(countries) > 0, "The list should not be empty"


@pytest.mark.dependency()
def test_all_countries_are_country_models():
    for i, country in enumerate(countries):
        assert isinstance(country, Country), f"Country at index {i} is not a Country Model"


@pytest.mark.dependency(depends=["test_all_countries_are_country_models"])
def test_first_country_has_name_key():
    assert hasattr(countries[0], "name"), "Attribute 'name' missing in first country"


@pytest.mark.dependency(depends=["test_all_countries_are_country_models"])
def test_first_country_has_alpha2code_key():
    assert hasattr(countries[0], "alpha2Code"), "Attribute 'alpha2Code' missing in first country"


@pytest.mark.dependency(depends=["test_all_countries_are_country_models"])
def test_first_country_has_region_key():
    assert hasattr(countries[0], "region"), "Attribute 'region' missing in first country"


@pytest.mark.dependency(depends=["test_all_countries_are_country_models"])
def test_print_first_random_last_country_names():
    first_name = getattr(countries[0], "name", None)
    last_name = getattr(countries[-1], "name", None)
    random_index = random.randint(0, len(countries) - 1)
    random_name = getattr(countries[random_index], "name", None)
    print(f"\nFirst country name: {first_name}")
    print(f"Random country name: {random_name}")
    print(f"Last country name: {last_name}\n")
