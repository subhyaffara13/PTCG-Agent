import os

def test_compression_size_fh(obj, method, compression_only, temp_file):
    path = temp_file
    with icom.get_handle(
        path,
        "w:gz" if compression_only == "tar" else "w",
        compression=compression_only,
    ) as handles:
        getattr(obj, method)(handles.handle)
        assert not handles.handle.closed
    compressed_size = os.path.getsize(path)

    # Create a new temporary file for uncompressed comparison
    path2 = temp_file.parent / f"{temp_file.stem}_uncompressed{temp_file.suffix}"
    path2.touch()
    with icom.get_handle(path2, "w", compression=None) as handles:
        getattr(obj, method)(handles.handle)
        assert not handles.handle.closed
    uncompressed_size = os.path.getsize(path2)
    assert uncompressed_size > compressed_size

