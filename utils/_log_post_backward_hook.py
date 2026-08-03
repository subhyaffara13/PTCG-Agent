import logging

def _log_post_backward_hook(
    state: _FSDPState, handle: "FlatParamHandle", logger: logging.Logger
) -> None:
    # Under TORCH_DISTRIBUTED_DEBUG=INFO, log the module names this hook fires for.
    # Below logging of module names this post-bwd hook fires for can help debug certain
    # cases where hooks don't fire, such as under certain activation checkpoint configs.
    if state._use_orig_params and handle._debug_level == dist.DebugLevel.INFO:
        param_fqns = _get_handle_fqns_from_root(state, handle)
        logger.warning("FSDP firing post-backward hooks for parameters %s", param_fqns)

