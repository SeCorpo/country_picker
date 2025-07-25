def dicts_loose_equivalent(a, b):
    """ Return True if a and b are 'loosely equal' dicts/lists (ignoring empty/null-equivalent values) """
    EMPTY_EQUIVALENTS = (None, [], {}, '')

    if isinstance(a, dict) and isinstance(b, dict):
        all_keys = set(a.keys()) | set(b.keys())
        for key in all_keys:
            va = a.get(key, None)
            vb = b.get(key, None)
            if va in EMPTY_EQUIVALENTS and vb in EMPTY_EQUIVALENTS:
                continue
            if not dicts_loose_equivalent(va, vb):
                return False
        return True

    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False
        # If all items are dicts, use key-based matching
        if all(isinstance(item, dict) for item in a + b):
            def has_matching_dict(item, candidates):
                MATCH_KEYS = ['acronym', 'code', 'name']
                for candidate in candidates:
                    if any(
                        item.get(k) == candidate.get(k)
                        for k in MATCH_KEYS
                        if k in item and k in candidate
                    ):
                        if dicts_loose_equivalent(item, candidate):
                            return True
                return False
            return (all(has_matching_dict(item, b) for item in a) and
                    all(has_matching_dict(item, a) for item in b))
        # Otherwise, compare by pair
        return all(dicts_loose_equivalent(x, y) for x, y in zip(a, b))

    if a in EMPTY_EQUIVALENTS and b in EMPTY_EQUIVALENTS:
        return True

    return a == b
