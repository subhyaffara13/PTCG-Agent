
def _full_post_load_state_dict_hook(
    module: nn.Module, fsdp_state: _FSDPState, *args, **kwargs
) -> None:
    if _should_unshard_params(fsdp_state):
        with SimpleProfiler.profile("_exit_unshard_params_ctx"):
            _exit_unshard_params_ctx(module, fsdp_state)

