
def valid_scalar_name(scalar_name: ScalarName | str) -> bool:
    """Return whether the given scalar name is a valid JIT scalar type name."""
    return scalar_name in _SCALAR_NAME_TO_TYPE

