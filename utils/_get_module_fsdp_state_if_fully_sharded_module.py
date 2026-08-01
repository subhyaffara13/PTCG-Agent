
def _get_module_fsdp_state_if_fully_sharded_module(
    module: nn.Module,
) -> _FSDPState | None:
    state = _get_module_fsdp_state(module)
    if state is None:
        return None
    if state == module:  # FullyShardedDataParallel module case.
        return state
    if module in state._fully_sharded_module_to_handle:  # fully_shard case.
        return state
    return None

