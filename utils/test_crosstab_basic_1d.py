
def test_crosstab_basic_1d(sparse):
    # Verify that a single input sequence works as expected.
    x = [1, 2, 3, 1, 2, 3, 3]
    expected_xvals = [1, 2, 3]
    expected_count = np.array([2, 2, 3])
    (xvals,), count = crosstab(x, sparse=sparse)
    assert_array_equal(xvals, expected_xvals)
    if sparse:
        assert_array_equal(count.toarray(), expected_count)
    else:
        assert_array_equal(count, expected_count)

