
def test_usecols_relative_to_names(all_parsers, names, usecols):
    data = """\
1,2,3
4,5,6
7,8,9
10,11,12"""
    parser = all_parsers
    if parser.engine == "pyarrow" and not isinstance(usecols[0], int):
        # ArrowKeyError: Column 'fb' in include_columns does not exist
        pytest.skip(reason="https://github.com/apache/arrow/issues/38676")

    result = parser.read_csv(StringIO(data), names=names, header=None, usecols=usecols)

    expected = DataFrame([[2, 3], [5, 6], [8, 9], [11, 12]], columns=["b", "c"])
    tm.assert_frame_equal(result, expected)

