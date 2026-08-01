
def _remapped_all_gather(*args, **kwargs):
    if not _are_we_tracing():
        raise AssertionError(
            "_remapped_all_gather should only be called during tracing"
        )
    all_gather_inplace(*args, **kwargs)

