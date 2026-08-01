
def test_select_where_datetime_index_with_non_ns_resolution(temp_hdfstore, unit):
    # GH#64310
    idx = date_range("2020-01-01", periods=10, freq="h", unit=unit)
    df = DataFrame({"value": range(10)}, index=idx)

    temp_hdfstore.append("df", df)

    result = temp_hdfstore.select(
        "df", where="index >= '2020-01-02' & index <= '2020-01-03'"
    )
    expected = df[(df.index >= "2020-01-02") & (df.index <= "2020-01-03")]
    tm.assert_frame_equal(result, expected)

