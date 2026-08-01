
def _get_array_element_type(tp: Type) -> ProperType | None:
    """Get the element type of the Array type tp, or None if not specified."""
    tp = get_proper_type(tp)
    if isinstance(tp, Instance):
        assert tp.type.fullname == "_ctypes.Array"
        if len(tp.args) == 1:
            return get_proper_type(tp.args[0])
    return None

