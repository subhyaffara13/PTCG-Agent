
def has_any_type(t: Type, ignore_in_type_obj: bool = False) -> bool:
    """Whether t contains an Any type"""
    return t.accept(HasAnyType(ignore_in_type_obj))

