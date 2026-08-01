
def test_iterator_skipfooter_errors(all_parsers, kwargs):
    msg = "'skipfooter' not supported for iteration"
    parser = all_parsers
    data = "a\n1\n2"

    if parser.engine == "pyarrow":
        msg = (
            "The '(chunksize|iterator)' option is not supported with the "
            "'pyarrow' engine"
        )

    with pytest.raises(ValueError, match=msg):
        with parser.read_csv(StringIO(data), skipfooter=1, **kwargs) as _:
            pass

