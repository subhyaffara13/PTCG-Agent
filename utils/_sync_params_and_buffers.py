
def _sync_params_and_buffers(
    process_group: dist.ProcessGroup,
    module_states: list[torch.Tensor],
    broadcast_bucket_size: int,
    src: int,
) -> None:
    """Synchronize ``module_states`` (list of tensors) across all processes by broadcasting them from rank 0."""
    if len(module_states) > 0:
        dist._broadcast_coalesced(
            process_group, module_states, broadcast_bucket_size, src
        )

