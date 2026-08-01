
def get_combined_dict(default_dict, additional_dict):
    """
    Combines two dictionaries.

    This function takes two dictionaries as input and returns a new dictionary
    that contains all the key-value pairs from both input dictionaries.
    If there are any duplicate keys in the `additional_dict`, the values
    from the `additional_dict` will overwrite those in the `default_dict`.
    Args:
        default_dict (dict): The main dictionary that will be used as the base
        additional_dict (dict): The dictionary used to update `default_dict`

    Returns:
        dict: The resulting dictionary
    Example:
        >>> x = dict(a=1, b=1)
        >>> y = dict(b=2, c=3)
        >>> get_combined_dict(x, y)
        {'a': 1, 'b': 2, 'c': 3}
    """
    d = default_dict.copy()
    d.update(additional_dict)
    return d

