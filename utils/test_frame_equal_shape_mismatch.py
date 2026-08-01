
def test_frame_equal_shape_mismatch(df1, df2, frame_or_series):
    df1 = DataFrame(df1)
    df2 = DataFrame(df2)
    msg = f"{frame_or_series.__name__} are different"

    with pytest.raises(AssertionError, match=msg):
        tm.assert_frame_equal(df1, df2, obj=frame_or_series.__name__)

