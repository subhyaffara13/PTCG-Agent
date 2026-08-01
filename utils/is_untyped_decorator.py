
def is_untyped_decorator(typ: Type | None) -> bool:
    typ = get_proper_type(typ)
    if not typ:
        return True
    elif isinstance(typ, CallableType):
        return not is_typed_callable(typ)
    elif isinstance(typ, Instance):
        method = typ.type.get_method("__call__")
        if method:
            if isinstance(method, Decorator):
                return is_untyped_decorator(method.func.type) or is_untyped_decorator(
                    method.var.type
                )

            if isinstance(method.type, Overloaded):
                return any(is_untyped_decorator(item) for item in method.type.items)
            else:
                return not is_typed_callable(method.type)
        else:
            return False
    elif isinstance(typ, Overloaded):
        return any(is_untyped_decorator(item) for item in typ.items)
    return True

