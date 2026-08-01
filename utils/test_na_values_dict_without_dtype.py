
def test_na_values_dict_without_dtype(all_parsers, na_values):
    parser = all_parsers
    data = """A
-99
-99
-99.0
-99.0"""

    result = parser.read_csv(StringIO(data), na_values=na_values)
    expected = DataFrame({"A": [np.nan, np.nan, np.nan, np.nan]})
    tm.assert_frame_equal(result, expected)

