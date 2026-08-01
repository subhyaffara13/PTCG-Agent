
def read_file_cached(blobpath: str, expected_hash: str | None = None) -> bytes:
    user_specified_cache = True
    if "TIKTOKEN_CACHE_DIR" in os.environ:
        cache_dir = os.environ["TIKTOKEN_CACHE_DIR"]
    elif "DATA_GYM_CACHE_DIR" in os.environ:
        cache_dir = os.environ["DATA_GYM_CACHE_DIR"]
    else:
        import tempfile

        cache_dir = os.path.join(tempfile.gettempdir(), "data-gym-cache")
        user_specified_cache = False

    if cache_dir == "":
        # disable caching
        return read_file(blobpath)

    cache_key = hashlib.sha1(blobpath.encode()).hexdigest()

    cache_path = os.path.join(cache_dir, cache_key)
    if os.path.exists(cache_path):
        with open(cache_path, "rb", buffering=0) as f:
            data = f.read()
        if expected_hash is None or check_hash(data, expected_hash):
            return data

        # the cached file does not match the hash, remove it and re-fetch
        try:
            os.remove(cache_path)
        except OSError:
            pass

    contents = read_file(blobpath)
    if expected_hash and not check_hash(contents, expected_hash):
        raise ValueError(
            f"Hash mismatch for data downloaded from {blobpath} (expected {expected_hash}). "
            f"This may indicate a corrupted download. Please try again."
        )

    import uuid

    try:
        os.makedirs(cache_dir, exist_ok=True)
        tmp_filename = cache_path + "." + str(uuid.uuid4()) + ".tmp"
        with open(tmp_filename, "wb") as f:
            f.write(contents)
        os.rename(tmp_filename, cache_path)
    except OSError:
        # don't raise if we can't write to the default cache, e.g. issue #75
        if user_specified_cache:
            raise

    return contents

