
def _remapped_allgather(*args, **kwargs):
    if not _are_we_tracing():
        raise AssertionError("_remapped_allgather should only be called during tracing")
    all_gather_tensor_inplace(*args, **kwargs)

