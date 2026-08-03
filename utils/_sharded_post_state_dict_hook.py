from typing import Any

def _sharded_post_state_dict_hook(
    module: nn.Module,
    fsdp_state: _FSDPState,
    state_dict: dict[str, Any],
    prefix: str,
) -> dict[str, Any]:
    """
    The hook replaces the unflattened, unsharded parameter in the state_dict
    with a unflattened, sharded parameter (a ShardedTensor).
    """

    def param_hook(state_dict: dict[str, Any], prefix: str, fqn: str):
        param = state_dict[fqn]
        if not fsdp_state._state_dict_config._use_dtensor:
            sharded_tensor = _ext_chunk_tensor(
                tensor=param,
                rank=fsdp_state.rank,
                world_size=fsdp_state.world_size,
                num_devices_per_node=fsdp_state._device_handle.device_count(),
                pg=fsdp_state.process_group,
                fsdp_extension=fsdp_state._fsdp_extension,
            )
        else:
            sharded_tensor = _ext_chunk_dtensor(
                tensor=param,
                rank=fsdp_state.rank,
                device_mesh=fsdp_state._device_mesh,
                fsdp_extension=fsdp_state._fsdp_extension,
            )
        if fsdp_state._state_dict_config.offload_to_cpu:
            sharded_tensor = sharded_tensor.cpu()
        state_dict[fqn] = sharded_tensor

    return _common_unshard_post_state_dict_hook(
        module, fsdp_state, state_dict, prefix, param_hook
    )

