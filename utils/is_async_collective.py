
def is_async_collective(snode):
    """
    Filtering out ops that contain Collective and Wait inside and considered as Collectives.
    See contains_collective function.
    If the op contains Wait inside - consider as Synchronous compute.
    """
    if python_kernel_name := getattr(snode.node, "python_kernel_name", None):
        if "torch.ops._dtensor.shard_dim_alltoall.default" in python_kernel_name:
            return False

    return True

