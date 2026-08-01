
def flatten_nested_tuples(types: Iterable[Type], handle_recursive: bool = True) -> list[Type]:
    """Recursively flatten TupleTypes nested with Unpack.

    For example this will transform
        Tuple[A, Unpack[Tuple[B, Unpack[Tuple[C, D]]]]]
    into
        Tuple[A, B, C, D]
    """
    res = []
    for typ in types:
        if not isinstance(typ, UnpackType):
            res.append(typ)
            continue
        p_type = get_proper_type(typ.type)
        if (
            not isinstance(p_type, TupleType)
            or not handle_recursive
            and isinstance(typ.type, TypeAliasType)
            and typ.type.is_recursive
        ):
            res.append(typ)
            continue
        if isinstance(typ.type, TypeAliasType):
            items = []
            for item in p_type.items:
                if (
                    isinstance(item, ProperType)
                    and isinstance(item, Instance)
                    or isinstance(item, TypeAliasType)
                ):
                    if len(item.args) == 0:
                        item = item.copy_modified()
                        item.set_line(typ)
                items.append(item)
        else:
            items = p_type.items
        res.extend(flatten_nested_tuples(items))
    return res

