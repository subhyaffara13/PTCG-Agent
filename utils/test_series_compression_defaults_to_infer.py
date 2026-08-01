
def test_series_compression_defaults_to_infer(
    write_method,
    write_kwargs,
    read_method,
    read_kwargs,
    compression_only,
    compression_to_extension,
    temp_file,
):
    # GH22004
    input = pd.Series([0, 5, -2, 10], name="X")
    extension = compression_to_extension[compression_only]
    path = temp_file.parent / f"compressed{extension}"
    getattr(input, write_method)(path, **write_kwargs)
    if "squeeze" in read_kwargs:
        kwargs = read_kwargs.copy()
        del kwargs["squeeze"]
        output = read_method(path, compression=compression_only, **kwargs).squeeze(
            "columns"
        )
    else:
        output = read_method(path, compression=compression_only, **read_kwargs)
    tm.assert_series_equal(output, input, check_names=False)

