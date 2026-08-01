
def _remapped_allreduce(*args, **kwargs):
    if not _are_we_tracing():
        raise AssertionError("_remapped_allreduce should only be called during tracing")
    all_reduce_inplace(*args, **kwargs)

