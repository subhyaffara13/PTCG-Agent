
def _sharded_post_load_state_dict_hook(
    module: nn.Module, fsdp_state: _FSDPState, *args, **kwargs
) -> None:
    if _has_fsdp_params(fsdp_state, module):
        with SimpleProfiler.profile("_exit_unshard_params_ctx"):
            _exit_unshard_params_ctx(module, fsdp_state)

