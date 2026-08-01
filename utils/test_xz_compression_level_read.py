
def test_xz_compression_level_read(obj, method, temp_file):
    path = temp_file
    getattr(obj, method)(path, compression="xz")
    compressed_size_default = os.path.getsize(path)
    getattr(obj, method)(path, compression={"method": "xz", "preset": 1})
    compressed_size_fast = os.path.getsize(path)
    assert compressed_size_default < compressed_size_fast
    if method == "to_csv":
        pd.read_csv(path, compression="xz")

