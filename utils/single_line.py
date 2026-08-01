
def single_line(val):
    """
    Quick and dirty validation for Summary pypa/setuptools#1390.
    """
    if '\n' in val:
        # TODO: Replace with `raise ValueError("newlines not allowed")`
        # after reviewing #2893.
        msg = "newlines are not allowed in `summary` and will break in the future"
        SetuptoolsDeprecationWarning.emit("Invalid config.", msg)
        # due_date is undefined. Controversial change, there was a lot of push back.
        val = val.strip().split('\n')[0]
    return val

