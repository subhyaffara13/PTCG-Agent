
def test_context_manageri_user_provided(all_parsers, datapath):
    # make sure that user-provided handles are not closed
    parser = all_parsers

    with open(datapath("io", "data", "csv", "iris.csv"), encoding="utf-8") as path:
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
            assert not reader.handles.handle.closed

