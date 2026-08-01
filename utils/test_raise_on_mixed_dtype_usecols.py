
def test_raise_on_mixed_dtype_usecols(all_parsers):
    # See gh-12678
    data = """a,b,c
        1000,2000,3000
        4000,5000,6000
        """
    usecols = [0, "b", 2]
    parser = all_parsers

    with pytest.raises(ValueError, match=_msg_validate_usecols_arg):
        parser.read_csv(StringIO(data), usecols=usecols)

