
def test_roundtrip_series_to_dataframe():
    categories = Series(["a", "b", "c", "a"])
    dummies = get_dummies(categories)
    result = from_dummies(dummies)
    expected = DataFrame({"": ["a", "b", "c", "a"]})
    tm.assert_frame_equal(result, expected)

