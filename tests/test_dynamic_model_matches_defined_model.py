from typing import Any, Dict, Type, List
from pydantic import BaseModel
from country_picker.core.models.country import Country
from country_picker.core.utils.dynamic_schema_from_response import dynamic_model_from_response
from country_picker.core.service.fetch_countries_raw import fetch_countries_raw

def test_dynamic_model_matches_defined_model():
    """
    Ensure the dynamic and defined Country models produce equivalent field structures

    Differences in field optionality (e.g., Optional, NoneType) are ignored,
    but missing fields in one model are reported as mismatches
    """
    raw_country_dicts = fetch_countries_raw()
    dynamic_country_model = dynamic_model_from_response(raw_country_dicts, model_name="Country")
    dynamic_model_fields = extract_field_structure(dynamic_country_model)
    defined_model_fields = extract_field_structure(Country)
    type_diffs, missing_attribute_diffs = find_field_structure_differences(dynamic_model_fields, defined_model_fields)

    print("DYNAMICALLY_GENERATED_PYDANTIC_SCHEMA_TREE:", dynamic_model_fields)
    if type_diffs:
        print("Dynamic and defined model field structures have type differences:\n")
        for diff in type_diffs:
            print(diff)
    if missing_attribute_diffs:
        print("\nTest failure: The following attributes are missing between models:")
        for diff in missing_attribute_diffs:
            print(diff)
        assert False

def find_field_structure_differences(dynamic_fields, defined_fields, parent_path=""):
    type_diffs = []
    missing_attr_diffs = []
    dynamic_keys = set(dynamic_fields.keys())
    defined_keys = set(defined_fields.keys())
    only_in_dynamic = dynamic_keys - defined_keys
    only_in_defined = defined_keys - dynamic_keys

    for key in only_in_dynamic:
        missing_attr_diffs.append(f"{parent_path}.{key if parent_path else key} is present in dynamic, missing in defined")
    for key in only_in_defined:
        missing_attr_diffs.append(f"{parent_path}.{key if parent_path else key} is present in defined, missing in dynamic")

    for key in dynamic_keys & defined_keys:
        dynamic_val = dynamic_fields.get(key)
        defined_val = defined_fields.get(key)
        current_path = f"{parent_path}.{key}" if parent_path else key

        if isinstance(dynamic_val, dict) and isinstance(defined_val, dict):
            sub_type_diffs, sub_missing_diffs = find_field_structure_differences(dynamic_val, defined_val, current_path)
            type_diffs += sub_type_diffs
            missing_attr_diffs += sub_missing_diffs
        elif isinstance(dynamic_val, list) and isinstance(defined_val, list):
            if dynamic_val and defined_val and isinstance(dynamic_val[0], dict) and isinstance(defined_val[0], dict):
                sub_type_diffs, sub_missing_diffs = find_field_structure_differences(dynamic_val[0], defined_val[0], current_path + "[0]")
                type_diffs += sub_type_diffs
                missing_attr_diffs += sub_missing_diffs
            elif dynamic_val != defined_val:
                if not are_optional_types_equivalent(dynamic_val[0], defined_val[0]):
                    type_diffs.append(
                        f"{current_path}:\n  dynamic:   {dynamic_val}\n  defined: {defined_val}"
                    )
        elif dynamic_val != defined_val:
            if not are_optional_types_equivalent(dynamic_val, defined_val):
                type_diffs.append(
                    f"{current_path}:\n  dynamic:   {dynamic_val}\n  defined: {defined_val}"
                )
    return type_diffs, missing_attr_diffs

def are_optional_types_equivalent(a, b):
    def normalize_type(type_str):
        type_str = str(type_str)
        return type_str.replace("Optional[", "").replace("]", "").replace("NoneType", "").strip()
    return (
        "Optional" in str(a) or "Optional" in str(b) or "NoneType" in str(a) or "NoneType" in str(b)
    ) and normalize_type(a) == normalize_type(b)

def extract_field_structure(model: Type[BaseModel]) -> Dict[str, Any]:
    structure = {}
    for field_name, field in model.model_fields.items():
        field_type = field.annotation
        origin = getattr(field_type, "__origin__", None)
        args = getattr(field_type, "__args__", ())
        if origin in (list, List):
            elem_type = args[0]
            if isinstance(elem_type, type) and issubclass(elem_type, BaseModel):
                structure[field_name] = [extract_field_structure(elem_type)]
            else:
                structure[field_name] = [str(getattr(elem_type, "__name__", str(elem_type)))]
        elif origin in (dict, Dict):
            value_type = args[1]
            if isinstance(value_type, type) and issubclass(value_type, BaseModel):
                structure[field_name] = {"dict": extract_field_structure(value_type)}
            else:
                structure[field_name] = {"dict": str(getattr(value_type, "__name__", str(value_type)))}
        elif isinstance(field_type, type) and issubclass(field_type, BaseModel):
            structure[field_name] = extract_field_structure(field_type)
        else:
            structure[field_name] = str(getattr(field_type, "__name__", str(field_type)))
    return structure
