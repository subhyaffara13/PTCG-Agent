
def test_apply_yield_list(float_frame):
    result = float_frame.apply(list)
    tm.assert_frame_equal(result, float_frame)

