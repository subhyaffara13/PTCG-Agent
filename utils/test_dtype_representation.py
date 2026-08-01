
def test_dtype_representation(using_infer_string):
    # GH#46900
    pmidx = MultiIndex.from_arrays([[1], ["a"]], names=[("a", "b"), ("c", "d")])
    result = pmidx.dtypes
    exp = "object" if not using_infer_string else pd.StringDtype(na_value=np.nan)
    expected = Series(
        ["int64", exp],
        index=MultiIndex.from_tuples([("a", "b"), ("c", "d")]),
        dtype=object,
    )
    tm.assert_series_equal(result, expected)

