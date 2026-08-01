
def patch_foreach_reduce(new_foreach_reduce: Callable):
    orig_foreach_foreach_reduce = (
        torch.distributed.fsdp._fully_shard._fsdp_param_group.foreach_reduce
    )
    dist.barrier()
    torch.distributed.fsdp._fully_shard._fsdp_param_group.foreach_reduce = (
        new_foreach_reduce
    )
    try:
        yield
    finally:
        dist.barrier()
        torch.distributed.fsdp._fully_shard._fsdp_param_group.foreach_reduce = (
            orig_foreach_foreach_reduce
        )

