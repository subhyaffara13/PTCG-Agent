
def test_unsupported_dtype(c_parser_only, match, kwargs, temp_file):
    parser = c_parser_only
    df = DataFrame(
        np.random.default_rng(2).random((5, 2)),
        columns=list("AB"),
        index=["1A", "1B", "1C", "1D", "1E"],
    )

    df.to_csv(temp_file)

    with pytest.raises(TypeError, match=match):
        parser.read_csv(temp_file, index_col=0, **kwargs)

