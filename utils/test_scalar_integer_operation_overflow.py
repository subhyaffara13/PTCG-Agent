
def test_scalar_integer_operation_overflow(dtype, operation):
    st = np.dtype(dtype).type
    min = st(np.iinfo(dtype).min)
    max = st(np.iinfo(dtype).max)

    with pytest.warns(RuntimeWarning, match="overflow encountered"):
        operation(min, max)

