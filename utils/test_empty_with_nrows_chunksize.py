
def test_empty_with_nrows_chunksize(all_parsers, iterator):
    # see gh-9535
    parser = all_parsers
    expected = DataFrame(columns=["foo", "bar"])

    nrows = 10
    data = StringIO("foo,bar\n")

    if parser.engine == "pyarrow":
        msg = (
            "The '(nrows|chunksize)' option is not supported with the 'pyarrow' engine"
        )
        with pytest.raises(ValueError, match=msg):
            if iterator:
                with parser.read_csv(data, chunksize=nrows) as reader:
                    next(iter(reader))
            else:
                parser.read_csv(data, nrows=nrows)
        return

    if iterator:
        with parser.read_csv(data, chunksize=nrows) as reader:
            result = next(iter(reader))
    else:
        result = parser.read_csv(data, nrows=nrows)

    tm.assert_frame_equal(result, expected)

