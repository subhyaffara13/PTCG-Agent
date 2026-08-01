
def test_context_manager(all_parsers, datapath):
    # make sure that opened files are closed
    parser = all_parsers

    path = datapath("io", "data", "csv", "iris.csv")

    if parser.engine == "pyarrow":
        msg = "The 'chunksize' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(path, chunksize=1)
        return

    reader = parser.read_csv(path, chunksize=1)
    assert not reader.handles.handle.closed
    try:
        with reader:
            next(reader)
            raise AssertionError
    except AssertionError:
        assert reader.handles.handle.closed

