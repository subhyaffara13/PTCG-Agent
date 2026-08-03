from typing import Any

def redistribute_bw_outputs(
    local_outs: Any, all_placements: Any, mesh: Any, _: int | None = None
) -> GraphArg:
    if len(local_outs) != len(all_placements):
        raise AssertionError(
            f"local_outs length ({len(local_outs)}) != all_placements length ({len(all_placements)})"
        )
    return _redistribute(
        local_outs,
        all_placements,
        mesh,
        torch.distributed.tensor._utils.compute_global_tensor_info,
    )

