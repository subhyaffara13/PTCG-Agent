
def _parse_arguments_into_strings(
    pos_only_store: dict[str, tuple[str | None, str | None]],
    kw_only_store: dict[str, tuple[str | None, str | None]],
) -> tuple[str, str]:
    """Parse positional and keyword arguments into strings for an __init__ method."""
    pos_only, kw_only = "", ""
    for pos_arg, data in pos_only_store.items():
        pos_only += pos_arg
        if data[0]:
            pos_only += ": " + data[0]
        if data[1]:
            pos_only += " = " + data[1]
        pos_only += ", "
    for kw_arg, data in kw_only_store.items():
        kw_only += kw_arg
        if data[0]:
            kw_only += ": " + data[0]
        if data[1]:
            kw_only += " = " + data[1]
        kw_only += ", "

    return pos_only, kw_only

