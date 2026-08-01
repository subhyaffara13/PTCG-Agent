
def is_python_scalar(x: object) -> TypeIs[complex]:  # numpydoc ignore=PR01,RT01
    """Return True if `x` is a Python scalar, False otherwise."""
    # isinstance(x, float) returns True for np.float64
    # isinstance(x, complex) returns True for np.complex128
    # bool is a subclass of int
    return isinstance(x, int | float | complex) and not is_numpy_array(x)


def is_python_scalar(val: Any) -> bool:
  return not isinstance(val, np.generic) and isinstance(val, (bool, int, float, complex))

