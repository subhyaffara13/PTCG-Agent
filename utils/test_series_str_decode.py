
def test_series_str_decode():
    # GH 22613
    result = Series([b"x", b"y"]).str.decode(encoding="UTF-8", errors="strict")
    expected = Series(["x", "y"], dtype="str")
    tm.assert_series_equal(result, expected)

