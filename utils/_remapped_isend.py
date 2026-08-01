
def _remapped_isend(*args, **kwargs):
    if not _are_we_tracing():
        raise AssertionError("_remapped_isend should only be called during tracing")
    return isend_inplace(*args, **kwargs)

