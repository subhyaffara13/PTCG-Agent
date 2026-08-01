
def get_default_loc_context(location=None):
    """
    Returns a context in which the defaulted location is created. If the location
    is None, takes the current location from the stack.
    """
    if location is None:
        if _cext.ir.Location.current:
            return _cext.ir.Location.current.context
        return None
    return location.context

