from typing import Any

def _post_load_state_dict_hook(
    module: nn.Module,
    incompatible_keys: tuple[list[str], list[str]],
    *args: Any,
) -> None:
    fsdp_state = _get_module_fsdp_state_if_fully_sharded_module(module)
    if fsdp_state.sharding_strategy == ShardingStrategy.NO_SHARD:
        context = _replace_with_full_state_dict_type(fsdp_state)
        warnings.warn(
            "When using ``NO_SHARD`` for ``ShardingStrategy``, full_state_dict will"
            "be returned.",
            stacklevel=2,
        )
    else:
        context = contextlib.nullcontext()

    with context:
        _post_load_state_dict_hook_fn = {
            StateDictType.FULL_STATE_DICT: _full_post_load_state_dict_hook,
            StateDictType.LOCAL_STATE_DICT: _local_post_load_state_dict_hook,
            StateDictType.SHARDED_STATE_DICT: _sharded_post_load_state_dict_hook,
        }
        # Code that is common for all state_dict impls
        # Dispatch into state_dict type specific implementation of post-hook for
        # loading state_dict.
        _post_load_state_dict_hook_fn[fsdp_state._state_dict_type](module, fsdp_state)

    # When reporting incompatible keys, trim FSDP prefixes.
    missing_keys = incompatible_keys[0]
    unexpected_keys = incompatible_keys[1]
    for i in range(len(missing_keys)):
        missing_keys[i] = clean_tensor_name(missing_keys[i])

    for i in range(len(unexpected_keys)):
        unexpected_keys[i] = clean_tensor_name(unexpected_keys[i])

    if fsdp_state._is_root:
        SimpleProfiler.dump_and_reset("FSDP model load_state_dict profiling: ")

