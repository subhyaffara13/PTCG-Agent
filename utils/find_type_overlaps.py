
def find_type_overlaps(*types: Type) -> set[str]:
    """Return a set of fullnames that share a short name and appear in either type.

    This is used to ensure that distinct types with the same short name are printed
    with their fullname.
    """
    d: dict[str, set[str]] = {}
    for type in types:
        for t in collect_all_named_types(type):
            if isinstance(t, ProperType) and isinstance(t, Instance):
                d.setdefault(t.type.name, set()).add(t.type.fullname)
            elif isinstance(t, TypeAliasType) and t.alias:
                d.setdefault(t.alias.name, set()).add(t.alias.fullname)
            else:
                assert isinstance(t, TypeVarLikeType)
                d.setdefault(t.name, set()).add(scoped_type_var_name(t))
    for shortname in d.keys():
        if f"typing.{shortname}" in TYPES_FOR_UNIMPORTED_HINTS:
            d[shortname].add(f"typing.{shortname}")

    overlaps: set[str] = set()
    for fullnames in d.values():
        if len(fullnames) > 1:
            overlaps.update(fullnames)
    return overlaps

