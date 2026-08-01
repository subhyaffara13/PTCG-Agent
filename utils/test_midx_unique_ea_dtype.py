
def test_midx_unique_ea_dtype():
    # GH#48335
    vals_a = Series([1, 2, NA, NA], dtype="Int64")
    vals_b = np.array([1, 2, 3, 3])
    midx = MultiIndex.from_arrays([vals_a, vals_b], names=["a", "b"])
    result = midx.unique()

    exp_vals_a = Series([1, 2, NA], dtype="Int64")
    exp_vals_b = np.array([1, 2, 3])
    expected = MultiIndex.from_arrays([exp_vals_a, exp_vals_b], names=["a", "b"])
    tm.assert_index_equal(result, expected)

