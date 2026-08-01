
def test_resample_empty_series_with_tz():
    # GH#53664
    df = DataFrame({"ts": [], "values": []}).astype(
        {"ts": "datetime64[ns, Atlantic/Faroe]"}
    )
    rs = df.resample("2MS", on="ts", closed="left", label="left")
    result = rs["values"].sum()

    expected_idx = DatetimeIndex(
        [], freq="2MS", name="ts", dtype="datetime64[ns, Atlantic/Faroe]"
    )
    expected = Series([], index=expected_idx, name="values", dtype="float64")
    tm.assert_series_equal(result, expected)

