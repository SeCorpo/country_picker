from country_picker.core.service.fetch_countries_dynamic import fetch_countries_dynamic
from country_picker.core.service.fetch_countries_raw import fetch_countries_raw
from country_picker.core.utils.dicts_loose_equivalent import dicts_loose_equivalent

def test_dynamic_country_model_matches_raw():
    """
    Test that each parsed country model, when converted back to a dict,
    is (loosely) equivalent to the corresponding original raw country dict from the API.

    "Loose equivalence" means differences between missing, None, and empty fields are ignored,
    and dicts within lists are compared by keys, not by order.
    """
    raw_country_dicts = fetch_countries_raw()
    dynamic_country_objs = fetch_countries_dynamic()
    dynamic_model_dicts = [
        country.model_dump(exclude_unset=False, exclude_defaults=False, exclude_none=False)
        for country in dynamic_country_objs
    ]

    assert len(raw_country_dicts) == len(dynamic_model_dicts), "Country list lengths do not match"

    for i in range(len(raw_country_dicts)):
        raw_country = raw_country_dicts[i]
        dynamic_dict = dynamic_model_dicts[i]
        for field in set(raw_country.keys()).union(dynamic_dict.keys()):
            raw_value = raw_country.get(field)
            parsed_value = dynamic_dict.get(field)
            if (raw_value in (None, [], {}, '') and parsed_value in (None, [], {}, '')):
                continue
            assert dicts_loose_equivalent(raw_value, parsed_value), (
                f"Mismatch at index {i}, field '{field}':\n"
                f"Raw: {raw_value!r}\n"
                f"Parsed: {parsed_value!r}"
            )
