
def _reinit_dispatch_logger():
    """
    Resets the cached DTensor dispatch logger state so that the next DTensor
    dispatch re-checks whether debug logging is enabled. Call this after
    changing the log level on the ``torch.distributed.tensor._dispatch`` logger.
    """
    torch._C._reinit_DTensor_dispatch_logger()

