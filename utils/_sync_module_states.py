
def _sync_module_states(
    module: nn.Module,
    process_group: dist.ProcessGroup,
    broadcast_bucket_size: int,
    src: int,
    params_and_buffers_to_ignore: Container[str],
    broadcast_buffers: bool = True,
) -> None:
    """
    Sync ``module``'s parameters and buffers state.

    Syncs ``module``'s parameters and buffers state so that all ranks contain
    the same module state across all ranks. Note that this API assumes that all
    parameter shapes are consistent before running the synchronization. This can
    be checked with ``_verify_param_shape_across_processes``.
    """
    module_states: list[torch.Tensor] = []
    for name, param in module.named_parameters():
        if name not in params_and_buffers_to_ignore:
            module_states.append(param.detach())

    if broadcast_buffers:
        for name, buffer in module.named_buffers():
            if name not in params_and_buffers_to_ignore:
                module_states.append(buffer.detach())

    _sync_params_and_buffers(process_group, module_states, broadcast_bucket_size, src)

