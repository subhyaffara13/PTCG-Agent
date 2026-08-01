
def test_nrows_skipfooter_errors(all_parsers):
    msg = "'skipfooter' not supported with 'nrows'"
    data = "a\n1\n2\n3\n4\n5\n6"
    parser = all_parsers

    with pytest.raises(ValueError, match=msg):
        parser.read_csv(StringIO(data), skipfooter=1, nrows=5)

