
def cache_dir() -> str:
    from torch._inductor.runtime.cache_dir_utils import cache_dir

    return cache_dir()


def cache_dir() -> str:
    cache_dir = os.environ.get("TORCHINDUCTOR_CACHE_DIR")
    if cache_dir is None:
        os.environ["TORCHINDUCTOR_CACHE_DIR"] = cache_dir = default_cache_dir()
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir

