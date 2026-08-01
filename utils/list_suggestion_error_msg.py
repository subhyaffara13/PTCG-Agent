
def list_suggestion_error_msg(name, potential, values):
    """
    Generate an error message that a potential setting is not an acceptable value.

    If the acceptable values are all strings, and sufficiently large, then add just a
    few suggestions to the end of the message. Otherwise list the supported values.

    Parameters
    ----------
    name : str
        The name of the setting, keyword argument, etc. to generate the message for.
    potential
        The potential value from the user that is not a valid choice.
    values : iterable
        Sequence of values to check on.
    """
    if len(values) > 5 and all(isinstance(v, str) for v in [potential, *values]):
        best = difflib.get_close_matches(potential, values, cutoff=0.5)
        match len(best):
            case 0:
                suggestion = ""
            case 1:
                suggestion = f" Did you mean: {best[0]!r}?"
            case _:
                suggestion = f" Did you mean one of: {', '.join(map(repr, best))}?"
    else:
        suggestion = f" Supported values are {', '.join(map(repr, values))}"
    return f"{potential!r} is not a valid value for {name}.{suggestion}"

