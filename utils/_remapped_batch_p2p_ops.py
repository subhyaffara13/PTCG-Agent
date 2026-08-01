
def _remapped_batch_p2p_ops(*args, **kwargs):
    if not _are_we_tracing():
        raise AssertionError(
            "_remapped_batch_p2p_ops should only be called during tracing"
        )
    return batch_p2p_ops_inplace(*args, **kwargs)

