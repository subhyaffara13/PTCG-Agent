
def test_union_with_duplicates(op):
    # GH#36289
    lvals = op([3, 1, 3, 4])
    rvals = op([2, 3, 1, 1])
    expected = op([3, 3, 1, 1, 4, 2])
    if isinstance(expected, np.ndarray):
        result = algos.union_with_duplicates(lvals, rvals)
        tm.assert_numpy_array_equal(result, expected)
    else:
        result = algos.union_with_duplicates(lvals, rvals)
        tm.assert_extension_array_equal(result, expected)

