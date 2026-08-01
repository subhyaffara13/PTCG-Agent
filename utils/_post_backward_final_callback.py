
def _post_backward_final_callback(
    state: _FSDPState,
    module: nn.Module,
):
    """
    This waits for the post-backward to finish and performs some final cleanup.
    This runs at the end of the entire backward pass and should only be called
    on the root FSDP instance.
    """
    _p_assert(
        state._is_root,
        "The post-backward callback should only be called on the root FSDP instance",
    )
    root_state = state

    if root_state._sync_gradients:
        current_stream = state._device_handle.current_stream()
        # TODO (rohan-varma): this also waits for the overlapped optimizer step to finish
        # since it currently runs in the post-backward stream. That can be
        # pushed to the next forward if run in a different stream
        current_stream.wait_stream(root_state._post_backward_stream)
        if root_state._all_reduce_stream is not current_stream:  # uses HSDP
            current_stream.wait_stream(root_state._all_reduce_stream)
        if root_state.cpu_offload.offload_params:
            # Wait for non-blocking GPU -> CPU sharded gradient copies from the
            # post-backward hooks to finish explicitly since CPU gradients do
            # not automatically synchronize with the GPU
            state._device_handle.current_stream().synchronize()
    root_state._exec_order_data.next_iter()

    for fsdp_state in state._all_fsdp_states:
        _catch_all_reshard(fsdp_state)
        _finalize_params(fsdp_state)
        fsdp_state.training_state = TrainingState.IDLE
        handle = fsdp_state._handle
        if handle:
            handle._ran_pre_backward_hook = False
            handle._needs_pre_backward_unshard = False
            handle._post_forward_index = None
            handle._training_state = HandleTrainingState.IDLE
            handle._prefetched = False
    # Reset for cases like one forward and multiple backwards
    root_state._post_backward_callback_queued = False

