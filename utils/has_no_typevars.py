
def has_no_typevars(typ: Type) -> bool:
    # We test if a type contains type variables by erasing all type variables
    # and comparing the result to the original type. We use comparison by equality that
    # in turn uses `__eq__` defined for types. Note: we can't use `is_same_type` because
    # it is not safe with unresolved forward references, while this function may be called
    # before forward references resolution patch pass. Note also that it is not safe to use
    # `is` comparison because `erase_typevars` doesn't preserve type identity.
    return typ == erase_typevars(typ)

