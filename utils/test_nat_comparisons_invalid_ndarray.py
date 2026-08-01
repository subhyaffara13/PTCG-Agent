
def test_nat_comparisons_invalid_ndarray(other):
    # GH#40722
    expected = np.array([False, False])
    result = NaT == other
    tm.assert_numpy_array_equal(result, expected)
    result = other == NaT
    tm.assert_numpy_array_equal(result, expected)

    expected = np.array([True, True])
    result = NaT != other
    tm.assert_numpy_array_equal(result, expected)
    result = other != NaT
    tm.assert_numpy_array_equal(result, expected)

    for symbol, op in [
        ("<=", operator.le),
        ("<", operator.lt),
        (">=", operator.ge),
        (">", operator.gt),
    ]:
        msg = f"'{symbol}' not supported between"

        with pytest.raises(TypeError, match=msg):
            op(NaT, other)

        if other.dtype == np.dtype("object"):
            # uses the reverse operator, so symbol changes
            msg = None
        with pytest.raises(TypeError, match=msg):
            op(other, NaT)

