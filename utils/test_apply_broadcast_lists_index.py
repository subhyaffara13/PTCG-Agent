
def test_apply_broadcast_lists_index(float_frame):
    result = float_frame.apply(
        lambda x: list(range(len(float_frame.index))), result_type="broadcast"
    )
    m = list(range(len(float_frame.index)))
    expected = DataFrame(
        dict.fromkeys(float_frame.columns, m),
        dtype="float64",
        index=float_frame.index,
    )
    tm.assert_frame_equal(result, expected)

