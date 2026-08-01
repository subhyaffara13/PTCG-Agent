
def zip_dicts(
    dict1: Mapping[KeyType, ValType],
    dict2: Mapping[KeyType, ValType],
    d1_default: ValType | None = None,
    d2_default: ValType | None = None,
) -> Generator[tuple[KeyType, ValType | None, ValType | None], None, None]:
    """
    Zip two dictionaries together, replacing missing keys with default values.

    Args:
        dict1 (dict): The first dictionary.
        dict2 (dict): The second dictionary.
        d1_default (Any): the default value for the first dictionary
        d2_default (Any): the default value for the second dictionary

    Yields:
        tuple: A tuple containing the key, the value from dict1 (or d1_default if missing),
               and the value from dict2 (or d2_default if missing).
    """
    # Find the union of all keys
    all_keys = OrderedSet(dict1.keys()) | OrderedSet(dict2.keys())

    # Iterate over all keys
    for key in all_keys:
        # Get the values from both dictionaries, or default if missing
        value1 = dict1.get(key)
        value2 = dict2.get(key)

        yield (
            key,
            value1 if value1 is not None else d1_default,
            value2 if value2 is not None else d2_default,
        )

