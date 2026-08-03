import os

def temporary_cache_dir(directory: str) -> Generator[None, None, None]:
    from torch._inductor.utils import clear_caches

    original = os.environ.get("TORCHINDUCTOR_CACHE_DIR")
    os.environ["TORCHINDUCTOR_CACHE_DIR"] = directory
    try:
        clear_caches()
        yield
    finally:
        clear_caches()
        if original is None:
            del os.environ["TORCHINDUCTOR_CACHE_DIR"]
        else:
            os.environ["TORCHINDUCTOR_CACHE_DIR"] = original

