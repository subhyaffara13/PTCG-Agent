
def _reshard(
    state: _FSDPState,
    handle: FlatParamHandle,
    free_unsharded_flat_param: bool,
):
    """
    Reshards the handle. ``free_unsharded_flat_param`` indicates whether to
    free the handle's padded unsharded flat parameter.
    """
    handle.reshard(free_unsharded_flat_param)
    if state.limit_all_gathers and free_unsharded_flat_param:
        if not torch.distributed._functional_collectives.is_torchdynamo_compiling():
            # We don't run a even queue for freeing under torch compile atm
            # But maybe we need to? TODO(voz): Look into this
            free_event = state._device_handle.Event()
            free_event.record()
            state._free_event_queue.enqueue(free_event)
    handle.post_reshard()
    # Flat parameter freed or not, we always have to "unshard" the parameter
    # upon next access to get its shape correct.
    handle._prefetched = False

