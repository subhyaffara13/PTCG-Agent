
def _reset_guarded_backend_cache() -> None:
    global cached_backends
    for backend in cached_backends.values():
        if hasattr(backend, "reset"):
            backend.reset()
    cached_backends.clear()

