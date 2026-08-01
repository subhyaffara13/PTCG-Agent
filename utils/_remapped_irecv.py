
def _remapped_irecv(*args, **kwargs):
    if not _are_we_tracing():
        raise AssertionError("_remapped_irecv should only be called during tracing")
    return irecv_inplace(*args, **kwargs)

