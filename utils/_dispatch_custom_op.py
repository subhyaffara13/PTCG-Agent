from typing import Callable

def _dispatch_custom_op(
    sharding_spec, op: Callable, types, args, kwargs, process_group
):
    """
    Calls the custom op for this ShardingSpec if it exists.
    """
    class_name = type(sharding_spec).__qualname__
    if not _has_custom_op(sharding_spec, op):
        raise RuntimeError(f"Custom op: {op} not registered for {class_name}")
    func = _CUSTOM_SHARDING_SPEC_OPS[class_name][op]
    return func(types, args, kwargs, process_group)

