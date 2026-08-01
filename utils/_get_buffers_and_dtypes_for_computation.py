
def _get_buffers_and_dtypes_for_computation(
    state: _FSDPState,
    root_module: nn.Module,
) -> tuple[list[torch.Tensor], list[torch.dtype | None]]:
    """
    Returns all buffers in the module tree rooted at ``root_module`` and a
    corresponding list of the buffer dtypes for computation. Each buffer dtype
    is either ``None`` if buffer mixed precision is not enabled or the buffer
    low precision dtype otherwise.
    """
    _p_assert(state._is_root, "Expects the root to cast buffers")
    buffers: list[torch.Tensor] = []
    buffer_dtypes: list[torch.dtype | None] = []
    visited_buffers: set[torch.Tensor] = set()
    # Traverse the FSDP states bottom-up so that we prefer the owning FSDP
    # instance's mixed precision setting for each buffer
    fsdp_states, fsdp_modules = traversal_utils._get_fsdp_states_with_modules(
        root_module
    )
    for fsdp_state, fsdp_module in zip(reversed(fsdp_states), reversed(fsdp_modules)):
        for buffer_name, buffer in fsdp_module.named_buffers():
            if buffer in visited_buffers:
                continue
            visited_buffers.add(buffer)
            if clean_tensor_name(buffer_name) in fsdp_state._ignored_buffer_names:
                continue
            buffers.append(buffer)
            buffer_dtypes.append(fsdp_state.mixed_precision.buffer_dtype)
    if len(buffers) != len(buffer_dtypes):
        raise AssertionError(
            f"Expected buffers and buffer_dtypes to have the same length, got {len(buffers)} and {len(buffer_dtypes)}"
        )
    return buffers, buffer_dtypes

