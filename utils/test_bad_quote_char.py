
def test_bad_quote_char(all_parsers, kwargs, msg):
    data = "1,2,3"
    parser = all_parsers

    with pytest.raises(TypeError, match=msg):
        parser.read_csv(StringIO(data), **kwargs)

