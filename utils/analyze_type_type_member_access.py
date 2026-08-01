
def analyze_type_type_member_access(
    name: str, typ: TypeType, mx: MemberContext, override_info: TypeInfo | None
) -> Type:
    # Similar to analyze_type_callable_attribute_access.
    item = None
    fallback = mx.named_type("builtins.type")
    if isinstance(typ.item, Instance):
        item = typ.item
    elif isinstance(typ.item, AnyType):
        with mx.msg.filter_errors():
            return _analyze_member_access(name, fallback, mx, override_info)
    elif isinstance(typ.item, TypeVarType):
        upper_bound = get_proper_type(typ.item.upper_bound)
        if isinstance(upper_bound, Instance):
            item = upper_bound
        elif isinstance(upper_bound, UnionType):
            return _analyze_member_access(
                name,
                TypeType.make_normalized(upper_bound, line=typ.line, column=typ.column),
                mx,
                override_info,
            )
        elif isinstance(upper_bound, TupleType):
            item = tuple_fallback(upper_bound)
        elif isinstance(upper_bound, AnyType):
            with mx.msg.filter_errors():
                return _analyze_member_access(name, fallback, mx, override_info)
    elif isinstance(typ.item, TupleType):
        item = tuple_fallback(typ.item)
    elif isinstance(typ.item, FunctionLike) and typ.item.is_type_obj():
        item = typ.item.fallback
    elif isinstance(typ.item, TypeType):
        # Access member on metaclass object via Type[Type[C]]
        if isinstance(typ.item.item, Instance):
            item = typ.item.item.type.metaclass_type
    ignore_messages = False

    if item is not None:
        fallback = item.type.metaclass_type or fallback

    if item and not mx.is_operator:
        # See comment above for why operators are skipped
        result = analyze_class_attribute_access(
            item, name, mx, mcs_fallback=fallback, override_info=override_info
        )
        if result:
            if not (isinstance(get_proper_type(result), AnyType) and item.type.fallback_to_any):
                return result
            else:
                # We don't want errors on metaclass lookup for classes with Any fallback
                ignore_messages = True

    with mx.msg.filter_errors(filter_errors=ignore_messages):
        return _analyze_member_access(name, fallback, mx, override_info)

