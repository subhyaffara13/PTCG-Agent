
def try_getting_literals_from_type(
    typ: Type, target_literal_type: type[T], target_fullname: str
) -> list[T] | None:
    """If the given expression or type corresponds to a Literal or
    union of Literals where the underlying values correspond to the given
    target type, returns a list of those underlying values. Otherwise,
    returns None.
    """
    typ = get_proper_type(typ)

    if isinstance(typ, Instance) and typ.last_known_value is not None:
        possible_literals: list[Type] = [typ.last_known_value]
    elif isinstance(typ, UnionType):
        possible_literals = list(typ.items)
    else:
        possible_literals = [typ]

    literals: list[T] = []
    for lit in get_proper_types(possible_literals):
        if isinstance(lit, LiteralType) and lit.fallback.type.fullname == target_fullname:
            val = lit.value
            if isinstance(val, target_literal_type):
                literals.append(val)
            else:
                return None
        else:
            return None
    return literals

