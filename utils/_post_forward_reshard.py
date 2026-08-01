
def _post_forward_reshard(
    state: _FSDPState,
    handle: FlatParamHandle,
) -> None:
    """Reshards parameters in the post-forward."""
    if not handle:
        return
    # Do not free the root's parameters in the post-forward for `FULL_SHARD`
    # with the intention that they are immediately used for backward
    # computation (though this may not be true)
    free_unsharded_flat_param = (
        not state._is_root
        and handle._sharding_strategy in RESHARD_AFTER_FORWARD_HANDLE_STRATEGIES
    )
    _reshard(state, handle, free_unsharded_flat_param)

