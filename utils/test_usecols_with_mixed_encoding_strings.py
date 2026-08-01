
def test_usecols_with_mixed_encoding_strings(all_parsers, usecols):
    data = """AAA,BBB,CCC,DDD
0.056674973,8,True,a
2.613230982,2,False,b
3.568935038,7,False,a"""
    parser = all_parsers
    _msg_validate_usecols_arg = (
        "'usecols' must either be list-like "
        "of all strings, all unicode, all "
        "integers or a callable."
    )
    with pytest.raises(ValueError, match=_msg_validate_usecols_arg):
        parser.read_csv(StringIO(data), usecols=usecols)

