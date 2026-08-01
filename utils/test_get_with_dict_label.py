
def test_get_with_dict_label():
    # GH47911
    s = Series(
        [
            {"name": "Hello", "value": "World"},
            {"name": "Goodbye", "value": "Planet"},
            {"value": "Sea"},
        ]
    )
    result = s.str.get("name")
    expected = Series(["Hello", "Goodbye", None], dtype=object)
    tm.assert_series_equal(result, expected)
    result = s.str.get("value")
    expected = Series(["World", "Planet", "Sea"], dtype=object)
    tm.assert_series_equal(result, expected)

