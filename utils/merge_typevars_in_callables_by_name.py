
def merge_typevars_in_callables_by_name(
    callables: Sequence[CallableType],
) -> tuple[list[CallableType], list[TypeVarType]]:
    """Takes all the typevars present in the callables and 'combines' the ones with the same name.

    For example, suppose we have two callables with signatures "f(x: T, y: S) -> T" and
    "f(x: List[Tuple[T, S]]) -> Tuple[T, S]". Both callables use typevars named "T" and
    "S", but we treat them as distinct, unrelated typevars. (E.g. they could both have
    distinct ids.)

    If we pass in both callables into this function, it returns a list containing two
    new callables that are identical in signature, but use the same underlying TypeVarType
    for T and S.

    This is useful if we want to take the output lists and "merge" them into one callable
    in some way -- for example, when unioning together overloads.

    Returns both the new list of callables and a list of all distinct TypeVarType objects used.
    """
    output: list[CallableType] = []
    unique_typevars: dict[str, TypeVarType] = {}
    variables: list[TypeVarType] = []

    for target in callables:
        if target.is_generic():
            target = freshen_function_type_vars(target)

            rename = {}  # Dict[TypeVarId, TypeVar]
            for tv in target.variables:
                name = tv.fullname
                if name not in unique_typevars:
                    # TODO: support ParamSpecType and TypeVarTuple.
                    if isinstance(tv, (ParamSpecType, TypeVarTupleType)):
                        continue
                    assert isinstance(tv, TypeVarType)
                    unique_typevars[name] = tv
                    variables.append(tv)
                rename[tv.id] = unique_typevars[name]

            target = expand_type(target, rename)
        output.append(target)

    return output, variables

