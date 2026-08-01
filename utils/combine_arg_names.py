
def combine_arg_names(
    t: CallableType | Parameters, s: CallableType | Parameters
) -> list[str | None]:
    """Produces a list of argument names compatible with both callables.

    For example, suppose 't' and 's' have the following signatures:

    - t: (a: int, b: str, X: str) -> None
    - s: (a: int, b: str, Y: str) -> None

    This function would return ["a", "b", None]. This information
    is then used above to compute the join of t and s, which results
    in a signature of (a: int, b: str, str) -> None.

    Note that the third argument's name is omitted and 't' and 's'
    are both valid subtypes of this inferred signature.

    Precondition: is_similar_types(t, s) is true.
    """
    num_args = len(t.arg_types)
    new_names = []
    for i in range(num_args):
        t_name = t.arg_names[i]
        s_name = s.arg_names[i]
        if t_name == s_name or t.arg_kinds[i].is_named() or s.arg_kinds[i].is_named():
            new_names.append(t_name)
        else:
            new_names.append(None)
    return new_names

