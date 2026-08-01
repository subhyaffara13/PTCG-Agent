
def _pre_load_state_dict_hook(
    module: nn.Module,
    state_dict: dict[str, Any],
    prefix: str,
    *args: Any,
) -> None:
    """
    This is called before ``module._load_from_state_dict()``.
    ``fsdp_state._state_dict_type`` is used to decide what preprocessing will
    be done.
    """
    fsdp_state = _get_module_fsdp_state_if_fully_sharded_module(module)
    if fsdp_state.sharding_strategy == ShardingStrategy.NO_SHARD:
        context = _replace_with_full_state_dict_type(fsdp_state)
        warnings.warn(
            "When using ``NO_SHARD`` for ``ShardingStrategy``, full_state_dict will"
            "be returned.",
            stacklevel=2,
        )
    else:
        _set_use_dtensor(fsdp_state)
        context = contextlib.nullcontext()

    _lazy_init(fsdp_state, module)
    if fsdp_state._is_root:
        SimpleProfiler.reset()

    with context:
        _pre_load_state_dict_hook_fn = {
            StateDictType.FULL_STATE_DICT: _full_pre_load_state_dict_hook,
            StateDictType.LOCAL_STATE_DICT: _local_pre_load_state_dict_hook,
            StateDictType.SHARDED_STATE_DICT: _sharded_pre_load_state_dict_hook,
        }
        # Code that is common for all state_dict impls
        if fsdp_state._device_handle.is_available():
            fsdp_state._device_handle.synchronize()
        # Dispatch into state_dict specific implementation of pre-hook.
        _pre_load_state_dict_hook_fn[fsdp_state._state_dict_type](
            module, fsdp_state, state_dict, prefix
        )

