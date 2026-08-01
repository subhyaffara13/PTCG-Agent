
def _enable_cp_dtensor_dispatcher() -> None:
    """Enables DTensor dispatcher to dispatch SDPA to CP."""
    # Enable custom op handlers for CP
    DTensor._op_dispatcher._custom_op_handlers = {
        **existing_custom_ops,
        **custom_ops,
    }
    # Register CP-specific sharding rules
    from ._sharding_rules import register_cp_sharding_rules

    register_cp_sharding_rules()

