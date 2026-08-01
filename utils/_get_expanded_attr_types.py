
def _get_expanded_attr_types(
    ctx: mypy.plugin.FunctionSigContext,
    typ: ProperType,
    display_typ: ProperType,
    parent_typ: ProperType,
) -> list[Mapping[str, Type]] | None:
    """
    For a given type, determine what attrs classes it can be: for each class, return the field types.
    For generic classes, the field types are expanded.
    If the type contains Any or a non-attrs type, returns None; in the latter case, also reports an error.
    """
    if isinstance(typ, AnyType):
        return None
    elif isinstance(typ, UnionType):
        ret: list[Mapping[str, Type]] | None = []
        for item in typ.relevant_items():
            item = get_proper_type(item)
            item_types = _get_expanded_attr_types(ctx, item, item, parent_typ)
            if ret is not None and item_types is not None:
                ret += item_types
            else:
                ret = None  # but keep iterating to emit all errors
        return ret
    elif isinstance(typ, TypeVarType):
        return _get_expanded_attr_types(
            ctx, get_proper_type(typ.upper_bound), display_typ, parent_typ
        )
    elif isinstance(typ, Instance):
        init_func = _get_attrs_init_type(typ)
        if init_func is None:
            _fail_not_attrs_class(ctx, display_typ, parent_typ)
            return None
        init_func = expand_type_by_instance(init_func, typ)
        # [1:] to skip the self argument of AttrClass.__init__
        field_names = cast(list[str], init_func.arg_names[1:])
        field_types = init_func.arg_types[1:]
        return [dict(zip(field_names, field_types))]
    else:
        _fail_not_attrs_class(ctx, display_typ, parent_typ)
        return None

