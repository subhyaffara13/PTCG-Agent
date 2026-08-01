
def try_getting_str_literals_from_type(typ: Type) -> list[str] | None:
    """If the given expression or type corresponds to a string Literal
    or a union of string Literals, returns a list of the underlying strings.
    Otherwise, returns None.

    For example, if we had the type 'Literal["foo", "bar"]' as input, this function
    would return a list of strings ["foo", "bar"].
    """
    return try_getting_literals_from_type(typ, str, "builtins.str")

