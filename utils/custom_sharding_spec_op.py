import functools

def custom_sharding_spec_op(sharding_spec_class, func):
    """
    Decorator to allow custom registration of ops.
    Args:
        sharding_spec_class(type): The ShardingSpec for which we need to add this custom op.
        func(Callable): The op to override (ex: torch.bmm)
    """
    class_name = sharding_spec_class.__qualname__
    if class_name not in _CUSTOM_SHARDING_SPEC_OPS:
        _CUSTOM_SHARDING_SPEC_OPS[class_name] = {}
    return functools.partial(
        _decorator_func, op=func, op_table=_CUSTOM_SHARDING_SPEC_OPS[class_name]
    )

