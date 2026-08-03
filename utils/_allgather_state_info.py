from typing import Any

def _allgather_state_info(
    fsdp_state: _FSDPState,
    input_states: dict[str, Any],
) -> list[dict[str, StateInfo]]:
    """
    Given the ``input_states``, allgather StateInfo for each state. The function
    uses all_gather_object to gather StateInfo so no GPU tensors are sent.
    """

    processed_state_dict: dict[str, StateInfo] = {}
    gathered_state_info: list[dict[str, StateInfo]] = [
        {} for _ in range(fsdp_state.world_size)
    ]

    for fqn, optim_state in input_states.items():
        # Allgather the scalar tensor state, non-tensor states and tensors metadata.
        processed_state = StateInfo({}, {}, {})
        for state_name, value in sorted_items(optim_state):
            if torch.is_tensor(value):
                if value.dim() == 0:
                    # Ensure that `step` is on CPU.
                    processed_state.scalar_tensors[state_name] = value.cpu()
                else:
                    processed_state.tensors[state_name] = _PosDimTensorInfo(
                        value.shape, value.dtype
                    )
            else:
                processed_state.non_tensors[state_name] = value
        processed_state_dict[fqn] = processed_state
    dist.all_gather_object(
        gathered_state_info,
        processed_state_dict,
        group=fsdp_state.process_group,
    )
    return gathered_state_info

