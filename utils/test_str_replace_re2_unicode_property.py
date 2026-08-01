
def test_str_replace_re2_unicode_property():
    ser = pd.Series(["Jan", "Feb", None], dtype=ArrowDtype(pa.string()))
    result = ser.str.replace(r"\p{Lu}", "U", regex=True)
    expected = pd.Series(["Uan", "Ueb", None], dtype=ArrowDtype(pa.string()))
    tm.assert_series_equal(result, expected)

