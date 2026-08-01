
def test_transform_dictlike(axis, float_frame, box):
    # GH 35964
    if axis in (0, "index"):
        e = float_frame.columns[0]
        expected = float_frame[[e]].transform(np.abs)
    else:
        e = float_frame.index[0]
        expected = float_frame.iloc[[0]].transform(np.abs)
    result = float_frame.transform(box({e: np.abs}), axis=axis)
    tm.assert_frame_equal(result, expected)


def test_transform_dictlike(string_series, box):
    # GH 35964
    with np.errstate(all="ignore"):
        expected = concat([np.sqrt(string_series), np.abs(string_series)], axis=1)
    expected.columns = ["foo", "bar"]
    result = string_series.transform(box({"foo": np.sqrt, "bar": np.abs}))
    tm.assert_frame_equal(result, expected)

