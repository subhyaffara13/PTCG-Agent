
def custom_special_method(typ: Type, name: str, check_all: bool = False) -> bool:
    """Does this type have a custom special method such as __format__() or __eq__()?

    If check_all is True ensure all items of a union have a custom method, not just some.
    """
    typ = get_proper_type(typ)
    if isinstance(typ, Instance):
        method = typ.type.get(name)
        if method and isinstance(method.node, (SYMBOL_FUNCBASE_TYPES, Decorator, Var)):
            if method.node.info:
                return not method.node.info.fullname.startswith(("builtins.", "typing."))
        return False
    if isinstance(typ, UnionType):
        if check_all:
            return all(custom_special_method(t, name, check_all) for t in typ.items)
        return any(custom_special_method(t, name) for t in typ.items)
    if isinstance(typ, TupleType):
        return custom_special_method(tuple_fallback(typ), name, check_all)
    if isinstance(typ, FunctionLike) and typ.is_type_obj():
        # Look up __method__ on the metaclass for class objects.
        return custom_special_method(typ.fallback, name, check_all)
    if isinstance(typ, TypeType) and isinstance(typ.item, Instance):
        if typ.item.type.metaclass_type:
            # Look up __method__ on the metaclass for class objects.
            return custom_special_method(typ.item.type.metaclass_type, name, check_all)
    if isinstance(typ, AnyType):
        # Avoid false positives in uncertain cases.
        return True
    # TODO: support other types (see ExpressionChecker.has_member())?
    return False

