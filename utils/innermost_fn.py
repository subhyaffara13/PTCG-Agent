
def innermost_fn(fn: Callable[..., Any]) -> Callable[..., Any]:
    """
    In case of nesting of _TorchDynamoContext calls, find the innermost
    function. TorchDynamo caches on fn.__code__ object, so its necessary to find
    the innermost function to pass on the optimize, run, disable etc.
    """
    unaltered_fn = fn
    while (
        hasattr(unaltered_fn, "_torchdynamo_orig_callable")
        # Only follow the chain if _torchdynamo_wrapper_id matches id(fn).
        # This prevents following chains in two cases:
        # 1. Bound methods: id(bound_method) != id(wrapper_function), so we
        #    won't unwrap through __func__ and lose the self binding.
        # 2. functools.wraps copies: When functools.wraps copies
        #    _torchdynamo_orig_callable from a wrapped function, the copied
        #    _torchdynamo_wrapper_id won't match the outer wrapper's id.
        and getattr(unaltered_fn, "_torchdynamo_wrapper_id", None) == id(unaltered_fn)
    ):
        unaltered_fn = unaltered_fn._torchdynamo_orig_callable
        assert callable(unaltered_fn), (
            f"A callable function is expected, but {type(unaltered_fn)} is provided."
        )
    return unaltered_fn

