
def test_read_unsupported_compression_type(temp_file):
    msg = "Unrecognized compression type: unsupported"
    with pytest.raises(ValueError, match=msg):
        pd.read_json(temp_file, compression="unsupported")

