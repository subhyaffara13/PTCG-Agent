
def is_unannotated_any(t: Type) -> bool:
    """Check if type represents an implicit (unannotated) Any.

    This is used to check for functions with unspecified/not fully specified types.
    """
    if not isinstance(t, ProperType):
        return False
    return isinstance(t, AnyType) and t.type_of_any == TypeOfAny.unannotated

