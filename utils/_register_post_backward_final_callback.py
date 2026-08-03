import functools

def _register_post_backward_final_callback(
    state: _FSDPState, module: nn.Module
) -> None:
    """
    Registers the post-backward final callback that runs at the end of the
    backward pass. This should be called from the root FSDP instance at the
    beginning of the pre-backward.
    """
    _p_assert(
        state._is_root,
        "Only the root FSDP instance should register the post-backward callback",
    )
    if state._post_backward_callback_queued:
        return
    _assert_in_training_states(state, [TrainingState.IDLE])
    # Trace does not need this callback
    if not torch.distributed._functional_collectives.is_torchdynamo_compiling():
        state._post_backward_callback_queued = True
        Variable._execution_engine.queue_callback(
            functools.partial(_post_backward_final_callback, state, module)
        )

