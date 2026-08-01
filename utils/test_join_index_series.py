
def test_join_index_series(float_frame):
    df = float_frame.copy()
    ser = df.pop(float_frame.columns[-1])
    joined = df.join(ser)

    tm.assert_frame_equal(joined, float_frame)

    ser.name = None
    with pytest.raises(ValueError, match="must have a name"):
        df.join(ser)

