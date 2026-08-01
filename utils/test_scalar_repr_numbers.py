
def test_scalar_repr_numbers(dtype, value):
    # Test NEP 51 scalar repr (and legacy option) for numeric types
    dtype = np.dtype(dtype)
    scalar = np.array(value, dtype=dtype)[()]
    assert isinstance(scalar, np.generic)

    string = str(scalar)
    repr_string = string.strip("()")  # complex may have extra brackets
    representation = repr(scalar)
    if dtype.char == "g":
        assert representation == f"np.longdouble('{repr_string}')"
    elif dtype.char == 'G':
        assert representation == f"np.clongdouble('{repr_string}')"
    else:
        normalized_name = np.dtype(f"{dtype.kind}{dtype.itemsize}").type.__name__
        assert representation == f"np.{normalized_name}({repr_string})"

    with np.printoptions(legacy="1.25"):
        assert repr(scalar) == string

