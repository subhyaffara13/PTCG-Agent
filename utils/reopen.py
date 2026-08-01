
def reopen(fs, path, mode, blocksize, loc, size, autocommit, cache_type, kwargs):
    file = fs.open(
        path,
        mode=mode,
        block_size=blocksize,
        autocommit=autocommit,
        cache_type=cache_type,
        size=size,
        **kwargs,
    )
    if loc > 0:
        file.seek(loc)
    return file


def reopen(fs: HfFileSystem, path: str, mode: str, block_size: int, cache_type: str):
    return fs.open(path, mode=mode, block_size=block_size, cache_type=cache_type)

