
def _disable_cp_dtensor_dispatcher() -> None:
    """Disables DTensor dispatcher to dispatch SDPA to CP."""
    # Restore original custom op handlers
    DTensor._op_dispatcher._custom_op_handlers = existing_custom_ops

    # TODO: unregister_cp_sharding_rules(clear_the_cache=True) will cause
    # all DTensor sharding propagation cache being invalidated. It is not
    # easy to achieve selectively invalidating lru cache without rewriting
    # the sharding propagation wrapper.

    from ._sharding_rules import unregister_cp_sharding_rules

    unregister_cp_sharding_rules(clear_the_cache=False)

