
def _exit_unshard_params_ctx(module: nn.Module, fsdp_state: _FSDPState) -> None:
    """A helper function to exit ``_unshard_fsdp_state_params`` context."""
    fsdp_state._unshard_params_ctx[module].__exit__(None, None, None)
    fsdp_state._unshard_params_ctx.pop(module)

