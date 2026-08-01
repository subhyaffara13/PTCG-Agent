
def test_dataframe_from_series_dont_infer_datetime():
    ser = Series([Timestamp("2019-12-31"), Timestamp("2020-12-31")], dtype=object)
    df = DataFrame(ser)
    assert df.dtypes.iloc[0] == np.dtype(object)
    assert np.shares_memory(get_array(ser), get_array(df, 0))
    assert not df._mgr._has_no_reference(0)

