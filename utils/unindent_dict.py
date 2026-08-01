
def unindent_dict(docdict: Mapping[str, str]) -> dict[str, str]:
    """Unindent all strings in a docdict.

    Parameters
    ----------
    docdict : dict[str, str]
        A dictionary with string values to unindent.

    Returns
    -------
    docdict : dict[str, str]
        The `docdict` dictionary but each of its string values are unindented.
    """
    can_dict: dict[str, str] = {}
    for name, dstr in docdict.items():
        can_dict[name] = unindent_string(dstr)
    return can_dict

