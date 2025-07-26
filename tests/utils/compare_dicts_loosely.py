from typing import Any, Dict, Tuple


EMPTY_MATCH_VALUES: Tuple[Any, ...] = (None, [], {}, '')

def compare_dicts_loosely(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    """
    Recursively compare two dictionaries for loose equivalence.

    Intended for comparing dynamic models (which include all fields discovered across the dataset)
    with raw API data, which may not define those fields at all in every dict.

    - Ignores differences between missing and empty-like values (None, [], {}, '')
    - Only compares keys where at least one of the values is meaningful
    - Recursively compares nested dictionaries and lists
    - List order is ignored (in _values_match)
    """
    if not isinstance(a, dict) or not isinstance(b, dict):
        raise TypeError("Both inputs must be dictionaries")

    for key in set(a) | set(b):
        # Does not include keys from nested dicts or inside list elements
        va = a.get(key)
        vb = b.get(key)

        if _is_empty(va) and _is_empty(vb):
            continue
        if not _values_match(va, vb):
            return False

    return True


def _values_match(a: Any, b: Any) -> bool:
    """
    Compare two values using loose matching rules

    - Dicts are compared recursively with dicts_loose_equivalent
    - Lists are compared without considering order. Each item in one list must match one item in the other
    """
    if isinstance(a, dict) and isinstance(b, dict):
        return compare_dicts_loosely(a, b)

    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False
        matched = [False] * len(b)
        for item_a in a:
            for i, item_b in enumerate(b):
                if not matched[i] and _values_match(item_a, item_b):
                    matched[i] = True
                    break
            else:
                return False
        return True

    return a == b


def _is_empty(value: Any) -> bool:
    """Check if a value is considered empty for loose matching."""
    return value in EMPTY_MATCH_VALUES
