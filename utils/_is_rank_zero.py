
def _is_rank_zero():
    """Return True if rank=0 or we aren't running distributed."""
    if not (_torch_distributed_available and torch.distributed.is_initialized()):
        return True
    return torch.distributed.get_rank() == 0

