
def test_dtypes_with_usecols(all_parsers):
    # GH#54868

    parser = all_parsers
    data = """a,b,c
1,2,3
4,5,6"""

    result = parser.read_csv(StringIO(data), usecols=["a", "c"], dtype={"a": object})
    if parser.engine == "pyarrow":
        values = [1, 4]
    else:
        values = ["1", "4"]
    expected = DataFrame({"a": pd.Series(values, dtype=object), "c": [3, 6]})
    tm.assert_frame_equal(result, expected)

