
def requires_nccl_shrink():
    """
    Require NCCL shrink support (NCCL available and version >= 2.27).
    """
    return requires_nccl_version((2, 27), "Need NCCL 2.27+ for shrink_group")

