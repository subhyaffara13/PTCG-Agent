
def filter_value_from_dict(dictionary: dict, key: str, depth: int = 0) -> Any:
    """
    Filters a value from a dictionary

    Goes through the nested dict and removes the key if it exists
    """
    from litellm.constants import DEFAULT_MAX_RECURSE_DEPTH

    if depth > DEFAULT_MAX_RECURSE_DEPTH:
        return dictionary

    # Create a copy of keys to avoid modifying dict during iteration
    keys = list(dictionary.keys())
    for k in keys:
        v = dictionary[k]
        if k == key:
            del dictionary[k]
        elif isinstance(v, dict):
            filter_value_from_dict(v, key, depth + 1)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    filter_value_from_dict(item, key, depth + 1)
    return dictionary

