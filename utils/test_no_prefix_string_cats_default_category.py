
def test_no_prefix_string_cats_default_category(
    default_category, expected, using_infer_string
):
    dummies = DataFrame({"a": [1, 0, 0], "b": [0, 1, 0]})
    result = from_dummies(dummies, default_category=default_category)
    expected = DataFrame(expected, dtype=dummies.columns.dtype)
    tm.assert_frame_equal(result, expected)

