
def test_usecols_with_integer_like_header(all_parsers, usecols, expected, request):
    parser = all_parsers
    data = """2,0,1
1000,2000,3000
4000,5000,6000"""

    if parser.engine == "pyarrow" and isinstance(usecols[0], int):
        with pytest.raises(ValueError, match=_msg_pyarrow_requires_names):
            parser.read_csv(StringIO(data), usecols=usecols)
        return

    result = parser.read_csv(StringIO(data), usecols=usecols)
    tm.assert_frame_equal(result, expected)

