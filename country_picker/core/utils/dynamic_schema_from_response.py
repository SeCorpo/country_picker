from typing import Any, Dict, List, Type, Optional, get_origin
from pydantic import BaseModel, create_model, Field

DEFAULT_EMPTY_LIST = Field(default_factory=list)
DEFAULT_EMPTY_DICT = Field(default_factory=dict)

def dynamic_model_from_response(
    data: List[Dict[str, Any]],
    model_name: str = "Country"
) -> Type[BaseModel]:
    """ Generates a dynamic Pydantic model from a list of dicts """
    structure = _generate_structure(data)
    return _build_pydantic_model(model_name, structure)

def _analyze_list_value_type(values):
    if not values:
        return Any
    if all(isinstance(item, dict) for item in values if item is not None):
        return dict
    types = set(type(item) for item in values if item is not None)
    if float in types or int in types:
        if all(isinstance(item, (int, float)) for item in values if item is not None):
            return float
    if str in types and len(types) == 1:
        return str
    if bool in types and len(types) == 1:
        return bool
    return Any

def _default_field_for_type(tp):
    origin = get_origin(tp) or tp
    if origin is list or tp is list:
        return DEFAULT_EMPTY_LIST
    if origin is dict or tp is dict:
        return DEFAULT_EMPTY_DICT
    return None

def _is_list_of_dicts(val):
    return isinstance(val, list) and bool(val) and all(isinstance(item, dict) for item in val if item is not None)

def _is_list_of_scalars(val):
    return isinstance(val, list) and not val or all(not isinstance(item, dict) for item in val if item is not None)

def _generate_structure(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    result = {}
    all_keys = set()
    for entry in data:
        all_keys.update(entry.keys())
    for key in all_keys:
        values = [item.get(key, None) for item in data if key in item]
        if any(isinstance(v, dict) for v in values if v is not None):
            dicts = [v for v in values if isinstance(v, dict)]
            result[key] = _generate_structure(dicts)
        elif any(_is_list_of_dicts(v) for v in values if v is not None):
            all_dicts = []
            for v in values:
                if _is_list_of_dicts(v):
                    all_dicts.extend(v)
            if all_dicts:
                merged = _generate_structure(all_dicts)
                result[key] = [merged]
            else:
                result[key] = []
        elif any(isinstance(v, list) for v in values if v is not None):
            all_scalars = []
            for v in values:
                if isinstance(v, list):
                    all_scalars.extend([x for x in v if not isinstance(x, dict)])
            result[key] = all_scalars
        else:
            first_non_none = next((v for v in values if v is not None), None)
            result[key] = first_non_none
    return result

def _build_pydantic_model(name: str, sample: Any) -> Type[BaseModel]:
    fields = {}
    if isinstance(sample, dict):
        for key, value in sample.items():
            if isinstance(value, dict):
                submodel = _build_pydantic_model(key.capitalize(), value)
                fields[key] = (Optional[submodel], None)
            elif _is_list_of_dicts(value):
                submodel = _build_pydantic_model(key.capitalize(), value[0] if value else {})
                fields[key] = (List[submodel], DEFAULT_EMPTY_LIST)
            elif _is_list_of_scalars(value):
                scalar_type = _analyze_list_value_type(value)
                fields[key] = (List[scalar_type], DEFAULT_EMPTY_LIST)
            else:
                scalar_type = type(value) if value is not None else Any
                if scalar_type in (int, float):
                    scalar_type = float
                fields[key] = (Optional[scalar_type], _default_field_for_type(scalar_type))
        return create_model(name, **fields)
    else:
        raise TypeError("Structure must be a dict at the root")
