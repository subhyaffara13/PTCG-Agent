
def string_to_scopes(scopes):
    """Converts stringifed scopes value to a list.

    Args:
        scopes (Union[Sequence, str]): The string of space-separated scopes
            to convert.
    Returns:
        Sequence(str): The separated scopes.
    """
    if not scopes:
        return []

    return scopes.split(" ")

