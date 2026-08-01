
def without_empty_values(input_dict):
    """
    Return a new dict not including empty value entries from `input_dict`.

    `None`, empty string, empty list, and empty dict/set are cleaned.
    `0` and `False` values are kept.
    """
    empty_values = ([], (), {}, "", None)

    return {key: value for key, value in input_dict.items() if value not in empty_values}

