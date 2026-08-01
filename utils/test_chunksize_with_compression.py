
def test_chunksize_with_compression(compression, temp_file):
    df = pd.read_json(StringIO('{"a": ["foo", "bar", "baz"], "b": [4, 5, 6]}'))
    df.to_json(temp_file, orient="records", lines=True, compression=compression)

    with pd.read_json(
        temp_file, lines=True, chunksize=1, compression=compression
    ) as res:
        roundtripped_df = pd.concat(res)
    tm.assert_frame_equal(df, roundtripped_df)

