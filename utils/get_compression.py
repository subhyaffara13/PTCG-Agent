
def get_compression(urlpath, compression):
    if compression == "infer":
        compression = infer_compression(urlpath)
    if compression is not None and compression not in compr:
        raise ValueError(f"Compression type {compression} not supported")
    return compression

