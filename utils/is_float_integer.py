
def is_float_integer(var: Any) -> bool:
    """Checks if a scalar variable is an integer or float (does not include bool)."""
    return np.issubdtype(type(var), np.integer) or np.issubdtype(type(var), np.floating)


def is_float_integer(var) -> bool:
    """Checks if a variable is an integer or float."""
    return np.issubdtype(type(var), np.integer) or np.issubdtype(type(var), np.floating)

