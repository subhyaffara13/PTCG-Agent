
def test_orc_uri_path(temp_file):
    expected = pd.DataFrame({"int": list(range(1, 4))})
    expected.to_orc(temp_file)
    uri = temp_file.as_uri()
    result = read_orc(uri)
    tm.assert_frame_equal(result, expected)

