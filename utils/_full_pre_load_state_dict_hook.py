
def _full_pre_load_state_dict_hook(
    module: nn.Module,
    fsdp_state: _FSDPState,
    state_dict: dict[str, Any],
    prefix: str,
) -> None:
    _lazy_init(fsdp_state, module)
    if _should_unshard_params(fsdp_state):
        with SimpleProfiler.profile("_enter_unshard_params_ctx"):
            _enter_unshard_params_ctx(module, fsdp_state, writeback=True)
    # Add FSDP_PREFIX only for wrapper-based FSDP.
    if not _is_composable(fsdp_state):
        _replace_by_prefix(state_dict, prefix, prefix + f"{FSDP_PREFIX}")

