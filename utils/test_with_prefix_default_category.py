
def test_with_prefix_default_category(
    dummies_with_unassigned, default_category, expected, using_infer_string
):
    result = from_dummies(
        dummies_with_unassigned, sep="_", default_category=default_category
    )
    expected = DataFrame(expected)
    if using_infer_string:
        expected = expected.astype("str")
    tm.assert_frame_equal(result, expected)

