
def test_scalar_signed_integer_overflow(dtype, operation):
    # The minimum signed integer can "overflow" for some additional operations
    st = np.dtype(dtype).type
    min = st(np.iinfo(dtype).min)
    neg_1 = st(-1)

    with pytest.warns(RuntimeWarning, match="overflow encountered"):
        operation(min, neg_1)

