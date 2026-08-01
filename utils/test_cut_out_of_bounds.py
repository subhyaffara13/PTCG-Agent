
def test_cut_out_of_bounds():
    arr = np.random.default_rng(2).standard_normal(100)
    result = cut(arr, [-1, 0, 1])

    mask = isna(result)
    ex_mask = (arr < -1) | (arr > 1)
    tm.assert_numpy_array_equal(mask, ex_mask)

