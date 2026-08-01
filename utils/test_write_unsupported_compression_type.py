
def test_write_unsupported_compression_type(temp_file):
    df = pd.read_json(StringIO('{"a": [1, 2, 3], "b": [4, 5, 6]}'))
    msg = "Unrecognized compression type: unsupported"
    with pytest.raises(ValueError, match=msg):
        df.to_json(temp_file, compression="unsupported")

