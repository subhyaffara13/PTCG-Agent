
def check_dict_or_set_indexers(key) -> None:
    """
    Check if the indexer is or contains a dict or set, which is no longer allowed.
    """
    if isinstance(key, set) or (
        isinstance(key, tuple) and any(isinstance(x, set) for x in key)
    ):
        raise TypeError(
            "Passing a set as an indexer is not supported. Use a list instead."
        )

    if isinstance(key, dict) or (
        isinstance(key, tuple) and any(isinstance(x, dict) for x in key)
    ):
        raise TypeError(
            "Passing a dict as an indexer is not supported. Use a list instead."
        )

