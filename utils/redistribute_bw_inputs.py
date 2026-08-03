from typing import Any

def redistribute_bw_inputs(
    global_args: Any, all_placements: Any, mesh: Any, num_activations: int
) -> GraphArg:
    if len(global_args) != len(all_placements) + num_activations:
        raise AssertionError(
            f"global_args length ({len(global_args)}) != "
            f"all_placements length ({len(all_placements)}) + num_activations ({num_activations})"
        )
    activations, inputs = global_args[:num_activations], global_args[num_activations:]
    if len(inputs) <= 0:
        raise AssertionError("inputs must not be empty")
    local_inputs = _redistribute(
        inputs,
        all_placements,
        mesh,
        torch.distributed.tensor._utils.compute_local_tensor_info,
    )
    return (
        *activations,
        *local_inputs,
    )

