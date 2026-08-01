
def test_transform_listlike(axis, float_frame, ops, names):
    # GH 35964
    other_axis = 1 if axis in {0, "index"} else 0
    with np.errstate(all="ignore"):
        expected = zip_frames([op(float_frame) for op in ops], axis=other_axis)
    if axis in {0, "index"}:
        expected.columns = MultiIndex.from_product([float_frame.columns, names])
    else:
        expected.index = MultiIndex.from_product([float_frame.index, names])
    result = float_frame.transform(ops, axis=axis)
    tm.assert_frame_equal(result, expected)


def test_transform_listlike(string_series, ops, names):
    # GH 35964
    with np.errstate(all="ignore"):
        expected = concat([op(string_series) for op in ops], axis=1)
        expected.columns = names
        result = string_series.transform(ops)
        tm.assert_frame_equal(result, expected)

