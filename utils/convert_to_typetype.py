
def convert_to_typetype(type_map: TypeMap) -> TypeMap:
    converted_type_map: dict[Expression, Type] = {}
    for expr, typ in type_map.items():
        t = typ
        if isinstance(t, TypeVarType):
            t = t.upper_bound
        t = get_proper_type(t)

        # TODO: should we only allow unions of instances as per PEP 484?
        if isinstance(t, UninhabitedType):
            converted_type_map[expr] = typ
        elif isinstance(t, (UnionType, Instance, NoneType)):
            converted_type_map[expr] = TypeType.make_normalized(typ)
        else:
            # unknown type; error was likely reported earlier
            return {}
    return converted_type_map

