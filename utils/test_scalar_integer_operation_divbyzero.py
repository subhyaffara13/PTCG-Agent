
def test_scalar_integer_operation_divbyzero(dtype, operation):
    st = np.dtype(dtype).type
    val = st(100)
    zero = st(0)

    with pytest.warns(RuntimeWarning, match="divide by zero"):
        operation(val, zero)

