
def test_dataframe_compression_defaults_to_infer(
    write_method,
    write_kwargs,
    read_method,
    compression_only,
    compression_to_extension,
    temp_file,
):
    # GH22004
    input = pd.DataFrame([[1.0, 0, -4], [3.4, 5, 2]], columns=["X", "Y", "Z"])
    extension = compression_to_extension[compression_only]
    path = temp_file.parent / f"compressed{extension}"
    getattr(input, write_method)(path, **write_kwargs)
    output = read_method(path, compression=compression_only)
    tm.assert_frame_equal(output, input)

