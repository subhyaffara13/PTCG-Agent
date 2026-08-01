
def test_file_truncated(tmp_path):
    path = tmp_path / "a.npy"
    for arr in basic_arrays:
        if arr.dtype != object:
            with open(path, 'wb') as f:
                format.write_array(f, arr)
            # truncate the file by one byte
            with open(path, 'rb+') as f:
                f.seek(-1, os.SEEK_END)
                f.truncate()
            with open(path, 'rb') as f:
                with pytest.raises(
                    ValueError,
                    match=(
                        r"EOF: reading array header, "
                        r"expected (\d+) bytes got (\d+)"
                    ) if arr.size == 0 else (
                        r"Failed to read all data for array\. "
                        r"Expected \(.*?\) = (\d+) elements, "
                        r"could only read (\d+) elements\. "
                        r"\(file seems not fully written\?\)"
                    )
                ):
                    _ = format.read_array(f)

