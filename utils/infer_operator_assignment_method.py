
def infer_operator_assignment_method(typ: Type, operator: str) -> tuple[bool, str]:
    """Determine if operator assignment on given value type is in-place, and the method name.

    For example, if operator is '+', return (True, '__iadd__') or (False, '__add__')
    depending on which method is supported by the type.
    """
    typ = get_proper_type(typ)
    method = operators.op_methods[operator]
    existing_method = None
    if isinstance(typ, Instance):
        existing_method = _find_inplace_method(typ, method, operator)
    elif isinstance(typ, TypedDictType):
        existing_method = _find_inplace_method(typ.fallback, method, operator)

    if existing_method is not None:
        return True, existing_method
    return False, method

