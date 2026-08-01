
def _copy_array_if_base_present(a):
    """Copy the array if its base points to a parent array."""
    if a.base is not None:
        return a.copy()
    return a

