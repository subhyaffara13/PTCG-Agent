
def test_map_pyarrow_timestamp(as_td):
    # GH#61231
    dti = date_range("2018-01-01 00:00:00", "2018-01-07 00:00:00")
    ser = Series(dti, dtype="timestamp[ns][pyarrow]", name="a")
    if as_td:
        # duration dtype
        ser = ser - ser[0]

    mapper = {date: i for i, date in enumerate(ser)}

    res_series = ser.map(mapper)
    expected = Series(range(len(ser)), name="a", dtype="int64")
    tm.assert_series_equal(res_series, expected)

    res_index = Index(ser).map(mapper)
    # For now (as of 2025-09-06) at least, we do inference on Index.map that
    #  we don't for Series.map
    expected_index = Index(expected).astype("int64[pyarrow]")
    tm.assert_index_equal(res_index, expected_index)

