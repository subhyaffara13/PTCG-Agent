
def test_to_json_compression_mode(compression):
    # GH 39985 (read_json does not support user-provided binary files)
    expected = pd.DataFrame({"A": [1]})

    with BytesIO() as buffer:
        expected.to_json(buffer, compression=compression)

