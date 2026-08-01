
def test_timestamp_dtype_matches_to_datetime():
    # GH#61775
    dtype1 = "datetime64[ns, US/Eastern]"
    dtype2 = "timestamp[ns, US/Eastern][pyarrow]"

    ts = pd.Timestamp("2025-07-03 18:10")

    result = pd.Series([ts], dtype=dtype2)
    expected = pd.Series([ts], dtype=dtype1).convert_dtypes(dtype_backend="pyarrow")

    tm.assert_series_equal(result, expected)

