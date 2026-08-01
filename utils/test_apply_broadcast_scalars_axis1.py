
def test_apply_broadcast_scalars_axis1(float_frame):
    result = float_frame.apply(np.mean, axis=1, result_type="broadcast")
    m = float_frame.mean(axis=1)
    expected = DataFrame(dict.fromkeys(float_frame.columns, m))
    tm.assert_frame_equal(result, expected)

