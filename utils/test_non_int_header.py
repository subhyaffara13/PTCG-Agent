
def test_non_int_header(all_parsers, header):
    # see gh-16338
    msg = "header must be integer or list of integers"
    data = """1,2\n3,4"""
    parser = all_parsers

    with pytest.raises(ValueError, match=msg):
        parser.read_csv(StringIO(data), header=header)

