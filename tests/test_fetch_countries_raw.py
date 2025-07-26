import random
import pytest
from country_picker.core.service.fetch_countries_raw import fetch_countries_raw

countries = fetch_countries_raw()

def test_countries_is_list():
    assert isinstance(countries, list), "fetch_countries_raw() should return a list"


def test_countries_not_empty():
    assert len(countries) > 0, "The list should not be empty"


@pytest.mark.dependency()
def test_all_countries_are_dicts():
    for i, country in enumerate(countries):
        assert isinstance(country, dict), f"Country at index {i} is not a dict"


@pytest.mark.dependency(depends=["test_all_countries_are_dicts"])
def test_all_countries_have_name_key():
    for i, country in enumerate(countries):
        assert "name" in country, f"Key 'name' missing in country dict at index {i}"


@pytest.mark.dependency(depends=["test_all_countries_are_dicts"])
def test_all_countries_have_alpha2code_key():
    for i, country in enumerate(countries):
        assert "alpha2Code" in country, f"Key 'alpha2Code' missing in country dict at index {i}"


@pytest.mark.dependency(depends=["test_all_countries_are_dicts"])
def test_all_countries_have_region_key():
    for i, country in enumerate(countries):
        assert "region" in country, f"Key 'region' missing in country dict at index {i}"


@pytest.mark.dependency(depends=["test_all_countries_are_dicts"])
def test_print_first_random_last_country_names():
    first_name = countries[0].get("name")
    last_name = countries[-1].get("name")
    random_index = random.randint(0, len(countries) - 1)
    random_name = countries[random_index].get("name")
    print(f"\nFirst country name: {first_name}")
    print(f"Random country name: {random_name}")
    print(f"Last country name: {last_name}\n")