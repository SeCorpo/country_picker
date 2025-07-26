from country_picker.core.service.fetch_countries_dynamic import fetch_countries_dynamic
from country_picker.core.service.fetch_countries_raw import fetch_countries_raw
from tests.utils.compare_dicts_loosely import compare_dicts_loosely


def test_dynamic_country_model_matches_raw():
    """
    Test that each parsed country model dict is loosely equivalent to the corresponding original raw dict

    The dynamically created model includes all possible fields (discovered across the dataset, from all raw dicts),
    whereas individual raw dicts may have some fields unset or set to empty values
    """
    raw_country_dicts = fetch_countries_raw()
    dynamic_country_objs = fetch_countries_dynamic()

    assert len(raw_country_dicts) == len(dynamic_country_objs), "Country list lengths do not match"

    #  assumes both raw and dynamic country lists are in the same order
    for i, (raw_country, model) in enumerate(zip(raw_country_dicts, dynamic_country_objs)):
        #  parse dynamic model instance back to dict (now with the extra fields from the generated 'general' dynamic model)
        parsed_dict = model.model_dump()
        assert compare_dicts_loosely(raw_country, parsed_dict), (
            f"Mismatch at index {i}:\n"
            f"Raw: {raw_country!r}\nParsed: {parsed_dict!r}"
        )
