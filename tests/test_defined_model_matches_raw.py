from country_picker.core.service.fetch_countries_raw import fetch_countries_raw
from country_picker.core.service.fetch_countries_defined import fetch_countries_defined
from tests.utils.compare_dicts_loosely import compare_dicts_loosely


def test_defined_country_model_matches_raw():
    """
    Test that each parsed defined country model dict is loosely equivalent to the corresponding original raw dict

    Ensure that for each country, the data parsed by the defined Country model remains (loosely) equivalent
    to the original raw country dictionary and no data is lost

    The defined model includes all possible fields (discovered across the dataset, from all raw dicts),
    whereas individual raw dicts may have some fields unset or set to empty values
    """
    raw_country_dicts = fetch_countries_raw()
    defined_country_objs = fetch_countries_defined()

    assert len(raw_country_dicts) == len(defined_country_objs), "Country list lengths do not match"

    #  assumes both raw and dynamic country lists are in the same order
    for i, (raw_country, model) in enumerate(zip(raw_country_dicts, defined_country_objs)):
        #  parse dynamic model instance back to dict (now with the extra fields from the generated 'general' dynamic model)
        parsed_dict = model.model_dump()
        assert compare_dicts_loosely(raw_country, parsed_dict), (
            f"Mismatch at index {i}:\n"
            f"Raw: {raw_country!r}\nParsed: {parsed_dict!r}"
        )