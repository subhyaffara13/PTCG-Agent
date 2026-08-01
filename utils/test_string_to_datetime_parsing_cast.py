
def test_string_to_datetime_parsing_cast():
    # GH 56266
    string_dates = ["2020-01-01 04:30:00", "2020-01-02 00:00:00", "2020-01-03 00:00:00"]
    result = pd.Series(string_dates, dtype="timestamp[s][pyarrow]")

    pd_res = pd.to_datetime(string_dates).as_unit("s")
    expected = pd.Series(ArrowExtensionArray(pa.array(pd_res, from_pandas=True)))
    tm.assert_series_equal(result, expected)

