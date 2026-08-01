
def torch_distributed_zero_first(local_rank: int):
    """
    Decorator to make all processes in distributed training wait for each local_master to do something.

    Args:
        local_rank (`int`): The rank of the local process.
    """
    if local_rank not in [-1, 0]:
        dist.barrier()
    yield
    if local_rank == 0:
        dist.barrier()


def torch_distributed_zero_first(*args, **kwargs):
    requires_backends(torch_distributed_zero_first, ["torch"])

