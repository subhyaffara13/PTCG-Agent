from typing import Any

def redistribute_fw_outputs(
    local_outs: Any, all_placements: Any, mesh: Any, num_activations: int
) -> GraphArg:
    if len(local_outs) != len(all_placements) + num_activations:
        raise AssertionError(
            f"local_outs length ({len(local_outs)}) != "
            f"all_placements length ({len(all_placements)}) + num_activations ({num_activations})"
        )
    num_fw_outs = len(local_outs) - num_activations
    if num_fw_outs <= 0:
        raise AssertionError(f"num_fw_outs must be > 0, got {num_fw_outs}")
    outs, activations = local_outs[:num_fw_outs], local_outs[num_fw_outs:]
    return (
        *_redistribute(
            outs,
            all_placements,
            mesh,
            torch.distributed.tensor._utils.compute_global_tensor_info,
        ),
        *activations,
    )

