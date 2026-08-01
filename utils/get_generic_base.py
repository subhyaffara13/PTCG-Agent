
def get_generic_base(cl):
    """If this is a generic class (A[str]), return the generic base for it."""
    if cl.__class__ is _GenericAlias:
        return cl.__origin__
    return None

