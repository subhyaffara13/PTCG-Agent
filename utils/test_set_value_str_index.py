
def test_set_value_str_index(string_series):
    # equiv
    ser = string_series.copy()
    res = ser._set_value("foobar", 0)
    assert res is None
    assert ser.index[-1] == "foobar"
    assert ser["foobar"] == 0

    ser2 = string_series.copy()
    ser2.loc["foobar"] = 0
    assert ser2.index[-1] == "foobar"
    assert ser2["foobar"] == 0

