
def _get_expanded_dataclasses_fields(
    ctx: FunctionSigContext, typ: ProperType, display_typ: ProperType, parent_typ: ProperType
) -> list[CallableType] | None:
    """
    For a given type, determine what dataclasses it can be: for each class, return the field types.
    For generic classes, the field types are expanded.
    If the type contains Any or a non-dataclass, returns None; in the latter case, also reports an error.
    """
    if isinstance(typ, UnionType):
        ret: list[CallableType] | None = []
        for item in typ.relevant_items():
            item = get_proper_type(item)
            item_types = _get_expanded_dataclasses_fields(ctx, item, item, parent_typ)
            if ret is not None and item_types is not None:
                ret += item_types
            else:
                ret = None  # but keep iterating to emit all errors
        return ret
    elif isinstance(typ, TypeVarType):
        return _get_expanded_dataclasses_fields(
            ctx, get_proper_type(typ.upper_bound), display_typ, parent_typ
        )
    elif isinstance(typ, Instance):
        replace_sym = typ.type.get_method(_INTERNAL_REPLACE_SYM_NAME)
        if replace_sym is None:
            return None
        replace_sig = replace_sym.type
        assert isinstance(replace_sig, ProperType)
        assert isinstance(replace_sig, CallableType)
        return [expand_type_by_instance(replace_sig, typ)]
    else:
        return None

