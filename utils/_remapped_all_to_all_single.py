
def _remapped_all_to_all_single(*args, **kwargs):
    if not _are_we_tracing():
        raise AssertionError(
            "_remapped_all_to_all_single should only be called during tracing"
        )
    all_to_all_inplace(*args, **kwargs)

