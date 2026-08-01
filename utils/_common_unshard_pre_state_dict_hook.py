
def _common_unshard_pre_state_dict_hook(
    module: nn.Module,
    fsdp_state: _FSDPState,
    offload_to_cpu: bool,
    rank0_only: bool,
) -> None:
    """
    Performs the pre-state_dict tasks shared by all state_dict types that require
    ``_unshard_fsdp_state_params()``. FULL_STATE_DICT and SHARDED_STATE_DICT use this hook.
    """
    # For composable `fully_shard`, it does not need to unshard parameters for `NO_SHARD` cases.
    if not _should_unshard_params(fsdp_state):
        return
    _enter_unshard_params_ctx(
        module,
        fsdp_state,
        writeback=False,
        offload_to_cpu=offload_to_cpu,
        rank0_only=rank0_only,
    )

