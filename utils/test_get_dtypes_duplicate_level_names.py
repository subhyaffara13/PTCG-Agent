
def test_get_dtypes_duplicate_level_names(using_infer_string):
    # Test MultiIndex.dtypes with non-unique level names (# GH45174)
    result = MultiIndex.from_product(
        [
            [1, 2, 3],
            ["a", "b", "c"],
            pd.date_range("20200101", periods=2, tz="UTC", unit="ns"),
        ],
        names=["A", "A", "A"],
    ).dtypes
    exp = "object" if not using_infer_string else pd.StringDtype(na_value=np.nan)
    expected = pd.Series(
        [np.dtype("int64"), exp, DatetimeTZDtype(tz="utc")],
        index=["A", "A", "A"],
    )
    tm.assert_series_equal(result, expected)

