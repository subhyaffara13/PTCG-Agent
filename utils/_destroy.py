
def _destroy(qualname):
    """De-registers a custom op. For testing purposes only"""
    custom_op = _find_custom_op(qualname)
    custom_op._destroy()

