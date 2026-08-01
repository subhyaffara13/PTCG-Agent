
def test_large_number():
    # GH#20608
    result = read_json(
        StringIO('["9999999999999999"]'),
        orient="values",
        typ="series",
        convert_dates=False,
    )
    expected = Series([9999999999999999])
    tm.assert_series_equal(result, expected)

