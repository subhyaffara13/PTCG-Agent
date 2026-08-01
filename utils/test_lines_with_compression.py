
def test_lines_with_compression(compression, temp_file):
    df = pd.read_json(StringIO('{"a": [1, 2, 3], "b": [4, 5, 6]}'))
    df.to_json(temp_file, orient="records", lines=True, compression=compression)
    roundtripped_df = pd.read_json(temp_file, lines=True, compression=compression)
    tm.assert_frame_equal(df, roundtripped_df)

