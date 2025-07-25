from country_picker.core.service.fetch_countries_raw import fetch_countries_raw
from country_picker.core.models.country import Country
from country_picker.core.utils.dicts_loose_equivalent import dicts_loose_equivalent

def test_defined_country_model_matches_raw():
    """
    Ensure that for each country, the data parsed by the defined Country model
    remains (loosely) equivalent to the original raw country dictionary.

    "Loose equivalence" means differences in missing, empty, None, or default fields are ignored,
    and dictionaries in lists are matched by content rather than by order.
    """
    raw_country_dicts = fetch_countries_raw()
    defined_country_objs = [Country.model_validate(country_dict) for country_dict in raw_country_dicts]
    defined_model_dicts = [
        obj.model_dump(exclude_unset=False, exclude_defaults=False, exclude_none=False)
        for obj in defined_country_objs
    ]
    for i, (raw_country, defined_dict) in enumerate(zip(raw_country_dicts, defined_model_dicts)):
        for field in set(raw_country.keys()).union(defined_dict.keys()):
            raw_value = raw_country.get(field)
            parsed_value = defined_dict.get(field)
            if (raw_value in (None, [], {}, '') and parsed_value in (None, [], {}, '')):
                continue
            assert dicts_loose_equivalent(raw_value, parsed_value), (
                f"Mismatch at index {i}, field '{field}':\n"
                f"Raw: {raw_value!r}\n"
                f"Parsed: {parsed_value!r}"
            )
