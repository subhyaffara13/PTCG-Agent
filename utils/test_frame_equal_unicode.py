
def test_frame_equal_unicode(df1, df2, msg, by_blocks_fixture, frame_or_series):
    # see gh-20503
    #
    # Test ensures that `tm.assert_frame_equals` raises the right exception
    # when comparing DataFrames containing differing unicode objects.
    df1 = DataFrame(df1)
    df2 = DataFrame(df2)
    msg = msg.format(obj=frame_or_series.__name__)
    with pytest.raises(AssertionError, match=msg):
        tm.assert_frame_equal(
            df1, df2, by_blocks=by_blocks_fixture, obj=frame_or_series.__name__
        )

