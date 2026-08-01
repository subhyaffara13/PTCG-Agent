
def is_main_process(local_rank):
    """
    Whether or not the current process is the local process, based on `xr.global_ordinal()` (for TPUs) first, then on
    `local_rank`.
    """
    if is_torch_xla_available():
        import torch_xla.runtime as xr

        return xr.global_ordinal() == 0
    return local_rank in [-1, 0]

