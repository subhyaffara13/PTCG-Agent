
def test_bzip_compression_level(obj, method, temp_file):
    """GH33196 bzip needs file size > 100k to show a size difference between
    compression levels, so here we just check if the call works when
    compression is passed as a dict.
    """
    path = temp_file
    getattr(obj, method)(path, compression={"method": "bz2", "compresslevel": 1})

