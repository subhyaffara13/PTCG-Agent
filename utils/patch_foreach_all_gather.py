from typing import Callable

def patch_foreach_all_gather(new_foreach_all_gather: Callable):
    orig_foreach_all_gather = (
        torch.distributed.fsdp._fully_shard._fsdp_param_group.foreach_all_gather
    )
    dist.barrier()
    torch.distributed.fsdp._fully_shard._fsdp_param_group.foreach_all_gather = (
        new_foreach_all_gather
    )
    try:
        yield
    finally:
        dist.barrier()
        torch.distributed.fsdp._fully_shard._fsdp_param_group.foreach_all_gather = (
            orig_foreach_all_gather
        )

