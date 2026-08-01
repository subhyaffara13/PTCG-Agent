
def _enter_unshard_params_ctx(
    module: nn.Module,
    fsdp_state: _FSDPState,
    writeback: bool = False,
    rank0_only: bool = False,
    offload_to_cpu: bool = False,
    with_grads: bool = False,
) -> None:
    """
    state_dict hooks cannot use the pure context call as the checkpoint flow
    requires to enter the context in the pre-hook but leave the context in the
    post-hook. This API enters the context of ``_unshard_fsdp_state_params``.
    """
    if module in fsdp_state._unshard_params_ctx:
        raise AssertionError(
            "Entering the ``_unshard_fsdp_state_params`` context but _unshard_params_ctx[module] "
            "is not None."
        )
    fsdp_state._unshard_params_ctx[module] = _unshard_fsdp_state_params(
        module,
        fsdp_state,
        writeback=writeback,
        rank0_only=rank0_only,
        offload_to_cpu=offload_to_cpu,
        with_grads=with_grads,
    )
    fsdp_state._unshard_params_ctx[module].__enter__()

