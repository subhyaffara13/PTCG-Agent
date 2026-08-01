
def make_format_string(func_name: str | None, groups: dict[ArgKind, list[RuntimeArg]]) -> str:
    """Return a format string that specifies the accepted arguments.

    The format string is an extended subset of what is supported by
    PyArg_ParseTupleAndKeywords(). Only the type 'O' is used, and we
    also support some extensions:

    - Required keyword-only arguments are introduced after '@'
    - If the function receives *args or **kwargs, we add a '%' prefix

    Each group requires the previous groups' delimiters to be present
    first.

    These are used by both vectorcall and legacy wrapper functions.
    """
    format = ""
    if groups[ARG_STAR] or groups[ARG_STAR2]:
        format += "%"
    format += "O" * len(groups[ARG_POS])
    if groups[ARG_OPT] or groups[ARG_NAMED_OPT] or groups[ARG_NAMED]:
        format += "|" + "O" * len(groups[ARG_OPT])
    if groups[ARG_NAMED_OPT] or groups[ARG_NAMED]:
        format += "$" + "O" * len(groups[ARG_NAMED_OPT])
    if groups[ARG_NAMED]:
        format += "@" + "O" * len(groups[ARG_NAMED])
    if func_name is not None:
        format += f":{func_name}"
    return format

