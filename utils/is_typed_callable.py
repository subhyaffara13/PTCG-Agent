
def is_typed_callable(c: Type | None) -> bool:
    c = get_proper_type(c)
    if not c or not isinstance(c, CallableType):
        return False
    return not all(
        isinstance(t, AnyType) and t.type_of_any == TypeOfAny.unannotated
        for t in get_proper_types(c.arg_types + [c.ret_type])
    )

