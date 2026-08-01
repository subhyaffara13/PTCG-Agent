
def _get_field_default(field_call: nodes.Call) -> _FieldDefaultReturn:
    """Return a the default value of a field call, and the corresponding keyword
    argument name.

    field(default=...) results in the ... node
    field(default_factory=...) results in a Call node with func ... and no arguments

    If neither or both arguments are present, return ("", None) instead,
    indicating that there is not a valid default value.
    """
    default, default_factory = None, None
    for keyword in field_call.keywords:
        if keyword.arg == "default":
            default = keyword.value
        elif keyword.arg == "default_factory":
            default_factory = keyword.value

    if default is not None and default_factory is None:
        return "default", default

    if default is None and default_factory is not None:
        new_call = nodes.Call(
            lineno=field_call.lineno,
            col_offset=field_call.col_offset,
            parent=field_call.parent,
            end_lineno=field_call.end_lineno,
            end_col_offset=field_call.end_col_offset,
        )
        new_call.postinit(func=default_factory, args=[], keywords=[])
        return "default_factory", new_call

    return None

