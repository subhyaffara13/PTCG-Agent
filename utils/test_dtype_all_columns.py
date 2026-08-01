
def test_dtype_all_columns(
    all_parsers, dtype, check_orig, using_infer_string, temp_file
):
    # see gh-3795, gh-6607
    parser = all_parsers

    df = DataFrame(
        np.random.default_rng(2).random((5, 2)).round(4),
        columns=list("AB"),
        index=["1A", "1B", "1C", "1D", "1E"],
    )

    df.to_csv(temp_file)

    result = parser.read_csv(temp_file, dtype=dtype, index_col=0)

    if check_orig:
        expected = df.copy()
        result = result.astype(float)
    elif using_infer_string and dtype is str:
        expected = df.astype(str)
    else:
        expected = df.astype(str).astype(object)

    tm.assert_frame_equal(result, expected)

