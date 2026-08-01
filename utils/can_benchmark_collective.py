
def can_benchmark_collective() -> bool:
    """Check if we can benchmark collectives (not fake process group)."""
    import torch.distributed as c10d

    if not c10d.is_initialized():
        return False

    pg = c10d.distributed_c10d._get_default_group()
    if (
        torch.distributed.distributed_c10d.get_backend(pg)
        == torch.distributed.distributed_c10d.Backend.FAKE
    ):
        return False

    return True

