
def test_apply_raw_float_frame_no_reduction(float_frame, engine):
    # no reduction
    result = float_frame.apply(lambda x: x * 2, engine=engine, raw=True)
    expected = float_frame * 2
    tm.assert_frame_equal(result, expected)

