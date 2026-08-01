
def test_usecols(all_parsers, usecols, request):
    data = """\
a,b,c
1,2,3
4,5,6
7,8,9
10,11,12"""
    parser = all_parsers
    if parser.engine == "pyarrow" and isinstance(usecols[0], int):
        with pytest.raises(ValueError, match=_msg_pyarrow_requires_names):
            parser.read_csv(StringIO(data), usecols=usecols)
        return

    result = parser.read_csv(StringIO(data), usecols=usecols)

    expected = DataFrame([[2, 3], [5, 6], [8, 9], [11, 12]], columns=["b", "c"])
    tm.assert_frame_equal(result, expected)

