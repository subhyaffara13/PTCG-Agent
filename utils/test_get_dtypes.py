
def test_get_dtypes(using_infer_string):
    # Test MultiIndex.dtypes (# Gh37062)
    idx_multitype = MultiIndex.from_product(
        [
            [1, 2, 3],
            ["a", "b", "c"],
            pd.date_range("20200101", periods=2, tz="UTC", unit="ns"),
        ],
        names=["int", "string", "dt"],
    )

    exp = "object" if not using_infer_string else pd.StringDtype(na_value=np.nan)
    expected = pd.Series(
        {
            "int": np.dtype("int64"),
            "string": exp,
            "dt": DatetimeTZDtype(tz="utc"),
        }
    )
    tm.assert_series_equal(expected, idx_multitype.dtypes)

