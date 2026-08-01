
def _hash_sensitive_info(data: Union[dict, list]) -> Union[dict, list, str]:
    """
    Hashes sensitive information within a dictionary.

    Args:
        data: The dictionary containing data to be processed.

    Returns:
        A new dictionary with sensitive values replaced by their SHA512 hashes.
        If the input is a list, returns a list with each element recursively processed.
        If the input is neither a dict nor a list, returns the type of the input as a string.

    """
    if isinstance(data, dict):
        hashed_data: Dict[Any, Union[Optional[str], dict, list]] = {}
        for key, value in data.items():
            if key in _SENSITIVE_FIELDS and not isinstance(value, (dict, list)):
                hashed_data[key] = _hash_value(value, key)
            elif isinstance(value, (dict, list)):
                hashed_data[key] = _hash_sensitive_info(value)
            else:
                hashed_data[key] = value
        return hashed_data
    elif isinstance(data, list):
        hashed_list = []
        for val in data:
            hashed_list.append(_hash_sensitive_info(val))
        return hashed_list
    else:
        # TODO(https://github.com/googleapis/google-auth-library-python/issues/1701):
        # Investigate and hash sensitive info before logging when the data type is
        # not a dict or a list.
        return str(type(data))

