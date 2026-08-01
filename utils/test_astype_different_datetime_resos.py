
def test_astype_different_datetime_resos():
    df = DataFrame({"a": date_range("2019-12-31", periods=2, freq="D")})
    result = df.astype("datetime64[ms]")

    assert not np.shares_memory(get_array(df, "a"), get_array(result, "a"))
    assert result._mgr._has_no_reference(0)

