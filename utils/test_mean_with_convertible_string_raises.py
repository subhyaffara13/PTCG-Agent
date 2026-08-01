
def test_mean_with_convertible_string_raises():
    # GH#44008
    ser = Series(["1", "2"])
    assert ser.sum() == "12"

    msg = "Could not convert string '12' to numeric|does not support|Cannot perform"
    with pytest.raises(TypeError, match=msg):
        ser.mean()

    df = ser.to_frame()
    msg = r"Could not convert \['12'\] to numeric|does not support|Cannot perform"
    with pytest.raises(TypeError, match=msg):
        df.mean()

