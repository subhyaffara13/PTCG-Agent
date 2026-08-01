
def test_invalid_compression(all_parsers, invalid_compression):
    parser = all_parsers
    compress_kwargs = {"compression": invalid_compression}

    msg = f"Unrecognized compression type: {invalid_compression}"

    with pytest.raises(ValueError, match=msg):
        parser.read_csv("test_file.zip", **compress_kwargs)

