
def _is_type_type(tp: ProperType) -> TypeGuard[TypeType | UnionType]:
    """Is ``tp`` a ``type[...]`` or a union thereof?

    ``Type[A | B]`` is internally represented as ``type[A] | type[B]``, and this
    troubles the solver sometimes.
    """
    return (
        isinstance(tp, TypeType)
        or isinstance(tp, UnionType)
        and all(isinstance(get_proper_type(o), TypeType) for o in tp.items)
    )

