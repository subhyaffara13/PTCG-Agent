from typing import Any

def _broadcast_state(
    fsdp_state: _FSDPState, state: Any, group: dist.ProcessGroup | None
) -> Any:
    if dist.get_rank(group) == 0:
        if not isinstance(state, torch.Tensor) or state.dim() == 0:
            return state
        tensor = state.to(fsdp_state.compute_device)
    else:
        if isinstance(state, torch.Tensor):
            if state.dim() != 0:
                raise AssertionError(
                    "For non-zero ranks, a tensor state should have zero dimension, "
                    f"but got the state with shape {state.shape}."
                )
            return state
        elif not isinstance(state, _PosDimTensorInfo):
            return state
        tensor = torch.zeros(
            state.shape, dtype=state.dtype, device=fsdp_state.compute_device
        )
    dist.broadcast(tensor, src=0, group=group)
    return tensor

