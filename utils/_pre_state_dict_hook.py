
def _pre_state_dict_hook(
    module: nn.Module,
    *args,
    **kwargs,
) -> None:
    """
    This is called before the core state dict saving logic of ``module``.
    ``fsdp_state._state_dict_type`` is used to decide what postprocessing will
    be done.
    """
    fsdp_state = _get_module_fsdp_state_if_fully_sharded_module(module)
    if fsdp_state.sharding_strategy == ShardingStrategy.NO_SHARD:
        context = _replace_with_full_state_dict_type(fsdp_state)
        warnings.warn(
            "When using ``NO_SHARD`` for ``ShardingStrategy``, full_state_dict will "
            "be returned.",
            stacklevel=2,
        )
    else:
        _set_use_dtensor(fsdp_state)
        context = contextlib.nullcontext()

    with context:
        _pre_state_dict_hook_fn = {
            StateDictType.FULL_STATE_DICT: _full_pre_state_dict_hook,
            StateDictType.LOCAL_STATE_DICT: _local_pre_state_dict_hook,
            StateDictType.SHARDED_STATE_DICT: _sharded_pre_state_dict_hook,
        }
        _pre_state_dict_hook_fn[fsdp_state._state_dict_type](
            fsdp_state,
            module,
            *args,
            **kwargs,
        )

