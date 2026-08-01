
def test_scalar_unsigned_integer_overflow(dtype):
    val = np.dtype(dtype).type(8)
    with pytest.warns(RuntimeWarning, match="overflow encountered"):
        -val

    zero = np.dtype(dtype).type(0)
    -zero  # does not warn

