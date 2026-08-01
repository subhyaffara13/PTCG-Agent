
def _has_custom_op(sharding_spec, op):
    """
    Returns whether or not the ShardingSpec has a custom op implementation.
    """
    class_name = type(sharding_spec).__qualname__
    return (
        class_name in _CUSTOM_SHARDING_SPEC_OPS
        and op in _CUSTOM_SHARDING_SPEC_OPS[class_name]
    )

