
def test_replace_compiled_regex_mixed_object():
    pat = re.compile(r"BAD_*")
    ser = Series(
        ["aBAD", np.nan, "bBAD", True, datetime.today(), "fooBAD", None, 1, 2.0]
    )
    result = Series(ser).str.replace(pat, "", regex=True)
    expected = Series(
        ["a", np.nan, "b", np.nan, np.nan, "foo", None, np.nan, np.nan], dtype=object
    )
    tm.assert_series_equal(result, expected)

