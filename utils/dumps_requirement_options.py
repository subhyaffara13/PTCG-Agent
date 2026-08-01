
def dumps_requirement_options(
    options,
    opt_string,
    quote_value=False,
    one_per_line=False,
):
    """
    Given a list of ``options`` and an ``opt_string``, return a string suitable
    for use in a pip requirements file. Raise Exception if any option name or
    value type is unknown.
    """
    option_items = []
    if quote_value:
        q = '"'
    else:
        q = ""

    if one_per_line:
        l = "\\\n    "
    else:
        l = ""

    for opt in options:
        if isinstance(opt, str):
            option_items.append(f"{l}{opt_string}={q}{opt}{q}")
        elif isinstance(opt, list):
            for val in sorted(opt):
                option_items.append(f"{l}{opt_string}={q}{val}{q}")
        else:
            raise Exception(
                f"Internal error: Unknown requirement option {opt!r} "
            )

    return " ".join(option_items)

