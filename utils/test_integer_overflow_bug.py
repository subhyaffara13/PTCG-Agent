
def test_integer_overflow_bug(all_parsers, sep):
    # see gh-2601
    data = "65248E10 11\n55555E55 22\n"
    parser = all_parsers
    if parser.engine == "pyarrow" and sep != " ":
        msg = "the 'pyarrow' engine does not support regex separators"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), header=None, sep=sep)
        return

    result = parser.read_csv(StringIO(data), header=None, sep=sep)
    expected = DataFrame([[6.5248e14, 11], [5.5555e59, 22]])
    tm.assert_frame_equal(result, expected)

