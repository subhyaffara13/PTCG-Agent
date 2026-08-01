
def test_str_dtype():
    # https://github.com/pandas-dev/pandas/pull/61623
    ser = pd.Series(["x", "y"], dtype="str")
    result = ser.explode()
    assert result is not ser
    tm.assert_series_equal(result, ser)


def test_str_dtype():
    # https://github.com/pandas-dev/pandas/pull/61623
    df = pd.DataFrame({"a": ["x", "y"]}, dtype="str")
    result = df.explode(column="a")
    assert result is not df
    tm.assert_frame_equal(result, df)

