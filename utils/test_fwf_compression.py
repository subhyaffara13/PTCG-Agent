
def test_fwf_compression(compression_only, infer, compression_to_extension, temp_file):
    data = """1111111111
    2222222222
    3333333333""".strip()

    compression = compression_only
    extension = compression_to_extension[compression]

    kwargs = {"widths": [5, 5], "names": ["one", "two"]}
    expected = read_fwf(StringIO(data), **kwargs)

    data = bytes(data, encoding="utf-8")

    path = temp_file.parent / f"tmp.{extension}"
    tm.write_to_compressed(compression, path, data)

    if infer is not None:
        kwargs["compression"] = "infer" if infer else compression

    result = read_fwf(path, **kwargs)
    tm.assert_frame_equal(result, expected)

