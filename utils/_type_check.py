
def _type_check(type1, type2) -> bool:
    if not all(map(has_known_bases, (type1, type2))):
        raise _NonDeducibleTypeHierarchy

    try:
        return type1 in type2.mro()[:-1]
    except MroError as e:
        # The MRO is invalid.
        raise _NonDeducibleTypeHierarchy from e

