
def test_callable_usecols(all_parsers, usecols, expected):
    # see gh-14154
    data = """AaA,bBb,CCC,ddd
0.056674973,8,True,a
2.613230982,2,False,b
3.568935038,7,False,a"""
    parser = all_parsers

    if parser.engine == "pyarrow":
        msg = "The pyarrow engine does not allow 'usecols' to be a callable"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), usecols=usecols)
        return

    result = parser.read_csv(StringIO(data), usecols=usecols)
    tm.assert_frame_equal(result, expected)

