
def test_to_frame_name_tuple_multiindex():
    idx = pd.Index([1])
    result = idx.to_frame(name=(1, 2))
    expected = pd.DataFrame([1], columns=MultiIndex.from_arrays([[1], [2]]), index=idx)
    tm.assert_frame_equal(result, expected)

