
def try_getting_int_literals_from_type(typ: Type) -> list[int] | None:
    """If the given expression or type corresponds to an int Literal
    or a union of int Literals, returns a list of the underlying ints.
    Otherwise, returns None.

    For example, if we had the type 'Literal[1, 2, 3]' as input, this function
    would return a list of ints [1, 2, 3].
    """
    return try_getting_literals_from_type(typ, int, "builtins.int")

