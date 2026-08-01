
def test_compression_size(obj, method, compression_only, temp_file):
    if compression_only == "tar":
        compression_only = {"method": "tar", "mode": "w:gz"}

    path = temp_file
    getattr(obj, method)(path, compression=compression_only)
    compressed_size = os.path.getsize(path)
    getattr(obj, method)(path, compression=None)
    uncompressed_size = os.path.getsize(path)
    assert uncompressed_size > compressed_size

