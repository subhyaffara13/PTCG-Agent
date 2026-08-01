
def _remapped_reducescatter(*args, **kwargs):
    if not _are_we_tracing():
        raise AssertionError(
            "_remapped_reducescatter should only be called during tracing"
        )
    reduce_scatter_tensor_inplace(*args, **kwargs)

