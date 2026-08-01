
def test_join_preserves_rangeindex(
    left, right, expected, expected_lidx, expected_ridx, how, right_type
):
    result, lidx, ridx = left.join(right_type(right), how=how, return_indexers=True)
    tm.assert_index_equal(result, expected, exact=True)

    if expected_lidx is None:
        assert lidx is expected_lidx
    else:
        exp_lidx = np.array(expected_lidx, dtype=np.intp)
        tm.assert_numpy_array_equal(lidx, exp_lidx)

    if expected_ridx is None:
        assert ridx is expected_ridx
    else:
        exp_ridx = np.array(expected_ridx, dtype=np.intp)
        tm.assert_numpy_array_equal(ridx, exp_ridx)

