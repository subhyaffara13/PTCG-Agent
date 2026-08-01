
def test_filename_with_special_chars(all_parsers, filename, tmp_path):
    # see gh-15086.
    parser = all_parsers
    df = DataFrame({"a": [1, 2, 3]})

    path = tmp_path / filename
    df.to_csv(path, index=False)

    result = parser.read_csv(path)
    tm.assert_frame_equal(result, df)

