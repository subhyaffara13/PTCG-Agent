
def test_compression_warning(compression_only, temp_file):
    # Assert that passing a file object to to_csv while explicitly specifying a
    # compression protocol triggers a RuntimeWarning, as per GH21227.
    df = pd.DataFrame(
        100 * [[0.123456, 0.234567, 0.567567], [12.32112, 123123.2, 321321.2]],
        columns=["X", "Y", "Z"],
    )
    path = temp_file
    with icom.get_handle(path, "w", compression=compression_only) as handles:
        with tm.assert_produces_warning(RuntimeWarning, match="has no effect"):
            df.to_csv(handles.handle, compression=compression_only)

