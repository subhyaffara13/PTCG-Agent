
def unknown_unpack(t: Type) -> bool:
    """Check if a given type is an unpack of an unknown type.

    Unfortunately, there is no robust way to distinguish forward references from
    genuine undefined names here. But this worked well so far, although it looks
    quite fragile.
    """
    if isinstance(t, UnpackType):
        unpacked = get_proper_type(t.type)
        if isinstance(unpacked, AnyType) and unpacked.type_of_any == TypeOfAny.special_form:
            return True
    return False

