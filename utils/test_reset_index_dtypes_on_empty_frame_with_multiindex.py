
def test_reset_index_dtypes_on_empty_frame_with_multiindex(
    array, dtype, using_infer_string
):
    # GH 19602 - Preserve dtype on empty DataFrame with MultiIndex
    idx = MultiIndex.from_product([[0, 1], [0.5, 1.0], array])
    result = DataFrame(index=idx)[:0].reset_index().dtypes
    if using_infer_string and dtype == object:
        dtype = pd.StringDtype(na_value=np.nan)
    expected = Series({"level_0": np.int64, "level_1": np.float64, "level_2": dtype})
    tm.assert_series_equal(result, expected)

