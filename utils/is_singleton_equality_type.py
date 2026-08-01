
def is_singleton_equality_type(typ: ProperType) -> bool:
    """
    Returns True if every value of this type compares equal to every other value of this type,
    as judged by the `==` operator.
    """
    return isinstance(typ, LiteralType) or is_singleton_identity_type(typ)

