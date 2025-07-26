from country_picker.core.service.fetch_countries_defined import fetch_countries_defined
from country_picker.core.service.fetch_countries_dynamic import fetch_countries_dynamic
from tests.utils.compare_dicts_loosely import compare_dicts_loosely


def test_defined_model_data_matches_dynamic_model_data():
    """
    Test that the data parsed to the defined model matches the data parsed to the dynamic model
    """
    defined_country_objs = fetch_countries_defined()
    dynamic_country_objs = fetch_countries_dynamic()

    assert len(defined_country_objs) == len(dynamic_country_objs), "Country list lengths do not match"

    #  assumes both defined and dynamic country lists are in the same order
    for i, (defined_model, dynamic_model) in enumerate(zip(defined_country_objs, dynamic_country_objs)):
        #  parse defined and dynamic model instance back to dict (now with the extra fields from
        #  the defined model and generated 'general' dynamic model)
        defined_model_parsed_dicts = defined_model.model_dump()
        dynamic_model_parsed_dicts = dynamic_model.model_dump()

        assert compare_dicts_loosely(defined_model_parsed_dicts, dynamic_model_parsed_dicts), (
            f"Mismatch at index {i}:\n"
            f"Raw: {defined_model_parsed_dicts!r}\nParsed: {dynamic_model_parsed_dicts!r}"
        )
