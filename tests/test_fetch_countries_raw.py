import random
import pytest
from country_picker.core.service.fetch_countries_raw import fetch_countries_raw

countries = fetch_countries_raw()

def test_countries_is_list():
    assert isinstance(countries, list), "fetch_countries_raw() should return a list"


def test_countries_not_empty():
    assert len(countries) > 0, "The list should not be empty"


@pytest.mark.dependency()
def test_first_country_is_dict():
    assert isinstance(countries[0], dict), "First country should be of type dict"


@pytest.mark.dependency(depends=["test_first_country_is_dict"])
def test_first_country_has_name_key():
    assert "name" in countries[0], "Key 'name' missing in first country dict"


@pytest.mark.dependency(depends=["test_first_country_is_dict"])
def test_first_country_has_alpha2code_key():
    assert "alpha2Code" in countries[0], "Key 'alpha2Code' missing in first country dict"


@pytest.mark.dependency(depends=["test_first_country_is_dict"])
def test_first_country_has_region_key():
    assert "region" in countries[0], "Key 'region' missing in first country dict"


@pytest.mark.dependency(depends=["test_first_country_is_dict"])
def test_print_first_random_last_country_names():
    first_name = countries[0].get("name")
    last_name = countries[-1].get("name")
    random_index = random.randint(0, len(countries) - 1)
    random_name = countries[random_index].get("name")
    print(f"\nFirst country name: {first_name}")
    print(f"Random country name: {random_name}")
    print(f"Last country name: {last_name}\n")