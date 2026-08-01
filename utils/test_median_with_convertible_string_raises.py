
def test_median_with_convertible_string_raises():
    # GH#34671 this _could_ return a string "2", but definitely not float 2.0
    msg = r"Cannot convert \['1' '2' '3'\] to numeric|does not support|Cannot perform"
    ser = Series(["1", "2", "3"])
    with pytest.raises(TypeError, match=msg):
        ser.median()

    msg = (
        r"Cannot convert \[\['1' '2' '3'\]\] to numeric|does not support|Cannot perform"
    )
    df = ser.to_frame()
    with pytest.raises(TypeError, match=msg):
        df.median()

