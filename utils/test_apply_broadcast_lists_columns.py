
def test_apply_broadcast_lists_columns(float_frame):
    # lists
    result = float_frame.apply(
        lambda x: list(range(len(float_frame.columns))),
        axis=1,
        result_type="broadcast",
    )
    m = list(range(len(float_frame.columns)))
    expected = DataFrame(
        [m] * len(float_frame.index),
        dtype="float64",
        index=float_frame.index,
        columns=float_frame.columns,
    )
    tm.assert_frame_equal(result, expected)

