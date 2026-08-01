
def test_fillna_with_none_object(test_frame, dtype):
    # GH#57723
    obj = Series([1, np.nan, 3], dtype=dtype)
    if test_frame:
        obj = obj.to_frame()
    result = obj.fillna(value=None)
    expected = Series([1, None, 3], dtype=dtype)
    if test_frame:
        expected = expected.to_frame()
    tm.assert_equal(result, expected)

