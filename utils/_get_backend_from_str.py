
def _get_backend_from_str(backend: str | None = None) -> Backend:
    # Default to the same backend as the global process group
    #  if backend is not specified.
    if not backend:
        backend = get_backend(_get_default_group())
    return Backend(backend)

