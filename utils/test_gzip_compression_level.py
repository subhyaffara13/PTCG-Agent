
def test_gzip_compression_level(obj, method, temp_file):
    # GH33196
    path = temp_file
    getattr(obj, method)(path, compression="gzip")
    compressed_size_default = os.path.getsize(path)
    getattr(obj, method)(path, compression={"method": "gzip", "compresslevel": 1})
    compressed_size_fast = os.path.getsize(path)
    assert compressed_size_default < compressed_size_fast

