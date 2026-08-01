
def _maybe_full_or_cpu_state_dict(
    state_dict: dict[str, Any], info: _StateDictInfo
) -> dict[str, Any]:
    if info.full_state_dict:
        ranks_only = (
            ()
            if (not info.cpu_offload or not torch.distributed.is_initialized())
            else (0,)
        )
        return _gather_state_dict(
            state_dict, cpu_offload=info.cpu_offload, ranks_only=ranks_only
        )
    elif info.cpu_offload:
        return _offload_state_dict_to_cpu(state_dict)
    else:
        return state_dict

