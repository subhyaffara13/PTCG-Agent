
def _clear_after_fork(cached):
    """Ensure ``func`` clears cached state after ``fork`` when supported.

    ``FastPath`` caches zip-backed ``pathlib.Path`` objects that retain a
    reference to the parent's open ``ZipFile`` handle. Re-using a cached
    instance in a forked child can therefore resurrect invalid file pointers
    and trigger ``BadZipFile``/``OSError`` failures (python/importlib_metadata#520).
    Registering ``cache_clear`` with ``os.register_at_fork`` keeps each process
    on its own cache.
    """
    getattr(os, 'register_at_fork', noop)(after_in_child=cached.cache_clear)


def _clear_after_fork(cached):
    """Ensure ``func`` clears cached state after ``fork`` when supported.

    ``FastPath`` caches zip-backed ``pathlib.Path`` objects that retain a
    reference to the parent's open ``ZipFile`` handle. Re-using a cached
    instance in a forked child can therefore resurrect invalid file pointers
    and trigger ``BadZipFile``/``OSError`` failures (python/importlib_metadata#520).
    Registering ``cache_clear`` with ``os.register_at_fork`` keeps each process
    on its own cache.
    """
    getattr(os, 'register_at_fork', noop)(after_in_child=cached.cache_clear)

