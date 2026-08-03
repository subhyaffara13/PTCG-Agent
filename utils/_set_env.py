import os

def _set_env(key: str, value: str) -> Iterator[None]:
    """Thread-safe env var set/restore using atomic C-level lookups.

    We avoid mock.patch.dict(os.environ, ...) because it internally calls
    os.environ.copy(), which iterates all env var keys then fetches values in
    separate steps. That approach is not atomic and can race with background threads
    (e.g. Triton async compilation) modifying the environment, causing KeyError,
    so we use os.environ.get() for individual keys which is an atomic C-level lookup.
    """
    old = os.environ.get(key)
    try:
        os.environ[key] = value
        yield
    finally:
        if old is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = old

