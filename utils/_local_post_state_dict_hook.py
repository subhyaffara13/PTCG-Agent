from typing import Any

def _local_post_state_dict_hook(
    module: nn.Module,
    fsdp_state: _FSDPState,
    state_dict: dict[str, Any],
    prefix: str,
) -> dict[str, Any]:
    """
    This hook create a ShardedTensor from the local flat_param and replace
    the state_dict[f"{prefix}{FLAT_PARAM}] with the ShardedTensor. No copy
    will happen. The underlying storage is the same.
    """

    _replace_by_prefix(state_dict, f"{prefix}{FSDP_PREFIX}", prefix)
    if not _has_fsdp_params(fsdp_state, module):
        return state_dict

    # state_dict[f"{prefix}{FLAT_PARAM}"] exists and has the same tensor
    # value as the flat_param but it is a pure Tensor because
    # nn.Module.state_dict() will detach the parameter. Therefore, we need
    # to get flat_param to get the metadata.
    if not _module_handle(fsdp_state, module):
        raise AssertionError("Should have returned early")
    flat_param = _module_handle(fsdp_state, module).flat_param
    # Constructs a ShardedTensor from the flat_param "without" padding.
    # Removing the padding allows users to change the number of ranks
    # when loading the local_state_dict.
    full_numel = flat_param._unpadded_unsharded_size.numel()  # type: ignore[attr-defined]
    shard_offset = flat_param.numel() * fsdp_state.rank
    valid_data_size = flat_param.numel() - flat_param._shard_numel_padded
    if valid_data_size > 0:
        # If FlatParameter is returned, FlatParameter._local_shard cause a
        # pickling issue (can be torch.save but not torch.load). Since there
        # is no benefit for state_dict to return the actual FlatParameter class,
        # a view (which is a tensor) of the FlatParameter will be returned.
        flat_param = flat_param[:valid_data_size].view(valid_data_size)
        local_shards = [
            Shard.from_tensor_and_offsets(flat_param, [shard_offset], fsdp_state.rank)
        ]
    else:
        local_shards = []
    sharded_tensor = init_from_local_shards(
        local_shards, full_numel, process_group=fsdp_state.process_group
    )  # type: ignore[assignment]
    # TODO: Add DTensor state_dict support for LOCAL_STATE_DICT.
    if fsdp_state._state_dict_config.offload_to_cpu:
        sharded_tensor = sharded_tensor.cpu()
    state_dict[f"{prefix}{FLAT_PARAM}"] = sharded_tensor
    return state_dict

