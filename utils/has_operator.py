
def has_operator(typ: Type, op_method: str) -> bool:
    """Does type have operator with the given name?

    Note: this follows the rules for operator access, in particular:
    * __getattr__ is not considered
    * for class objects we only look in metaclass
    * instance level attributes (i.e. extra_attrs) are not considered
    """
    # This is much faster than analyze_member_access, and so using
    # it first as a filter is important for performance. This is mostly relevant
    # in situations where we can't expect that method is likely present,
    # e.g. for __OP__ vs __rOP__.
    typ = get_proper_type(typ)

    if isinstance(typ, TypeVarLikeType):
        typ = typ.values_or_bound()
    if isinstance(typ, AnyType):
        return True
    if isinstance(typ, UnionType):
        return all(has_operator(x, op_method) for x in typ.relevant_items())
    if isinstance(typ, FunctionLike) and typ.is_type_obj():
        return typ.fallback.type.has_readable_member(op_method)
    if isinstance(typ, TypeType):
        # Type[Union[X, ...]] is always normalized to Union[Type[X], ...],
        # so we don't need to care about unions here, but we need to care about
        # Type[T], where upper bound of T is a union.
        item = typ.item
        if isinstance(item, TypeVarType):
            item = item.values_or_bound()
        if isinstance(item, UnionType):
            return all(meta_has_operator(x, op_method) for x in item.relevant_items())
        return meta_has_operator(item, op_method)
    return instance_fallback(typ).type.has_readable_member(op_method)

