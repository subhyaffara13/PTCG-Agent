
def test_read_chunksize_jagged_names(all_parsers):
    # see gh-23509
    parser = all_parsers
    data = "\n".join(["0"] * 7 + [",".join(["0"] * 10)])

    expected = DataFrame([[0] + [np.nan] * 9] * 7 + [[0] * 10])

    if parser.engine == "pyarrow":
        msg = "The 'chunksize' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            with parser.read_csv(
                StringIO(data), names=range(10), chunksize=4
            ) as reader:
                concat(reader)
        return

    with parser.read_csv(StringIO(data), names=range(10), chunksize=4) as reader:
        result = concat(reader)
    tm.assert_frame_equal(result, expected)

