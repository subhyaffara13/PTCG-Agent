import os
import math


def _should_use_fused_all_gather_matmul_native(
    A_shard: torch.Tensor,
    Bs: list[torch.Tensor],
    gather_dim: int,
    group_name: c10d.GroupName,
) -> bool:
    group = c10d._resolve_process_group(group_name)
    local_M = math.prod(A_shard.shape[:-1])

    return (
        "TORCH_SYMM_MEM_ENABLE_NATIVE_ASYNC_TP" in os.environ
        and A_shard.is_contiguous()
        and gather_dim == 0
        # _async_input_mm requires local_M to be divisible by world_size.
        and local_M % group.size() == 0
        # _async_input_mm outperforms the decomposition-based approach when the
        # global M is small.
        and 2048 < local_M * group.size() <= 4096
        # _async_input_mm only supports a single B.
        and len(Bs) == 1
    )

