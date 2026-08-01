
def is_typeddict_type_context(lvalue_type: Type) -> bool:
    lvalue_type = get_proper_type(lvalue_type)
    if isinstance(lvalue_type, TypedDictType):
        return True
    if isinstance(lvalue_type, UnionType):
        for item in lvalue_type.items:
            if is_typeddict_type_context(item):
                return True
    return False

