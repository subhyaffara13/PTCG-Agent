
def test_to_json_compression(
    compression_only,
    read_infer,
    to_infer,
    compression_to_extension,
    infer_string,
    tmp_path,
):
    with pd.option_context("future.infer_string", infer_string):
        # see gh-15008
        compression = compression_only

        # We'll complete file extension subsequently.
        filename = tmp_path / f"test.{compression_to_extension[compression]}"

        df = pd.DataFrame({"A": [1]})

        to_compression = "infer" if to_infer else compression
        read_compression = "infer" if read_infer else compression

        df.to_json(filename, compression=to_compression)
        result = pd.read_json(filename, compression=read_compression)
        tm.assert_frame_equal(result, df)

