
def mark_subclass_constructor_exportable_experimental(constructor_subclass):
    """
    Experimental decorator that makes subclass to be traceable in export
    with pre-dispatch IR. To make your subclass traceble in export, you need to:
        1. Implement __init__ method for your subclass (Look at DTensor implementation)
        2. Decorate your __init__ method with _mark_constructor_exportable_experimental
        3. Put torch._dynamo_disable decorator to prevent dynamo from peeking into its' impl

    Example:

    class FooTensor(torch.Tensor):
        @staticmethod
        def __new__(cls, elem, *, requires_grad=False):
            # ...
            return torch.Tensor._make_subclass(cls, elem, requires_grad=requires_grad)

        @torch._dynamo_disable
        @mark_subclass_constructor_exportable_experimental
        def __init__(self, elem, ...):
            # ...
    """
    if not _is_init(constructor_subclass):
        raise RuntimeError(
            f"torch._export.wrappers.mark_constructor_exportable_experimental can only be applied on subclass tensor.__init__"
            f"But, you are adding it on {constructor_subclass.__name__} which is not supported. "
            f"If __init__ doesn't exist on your subclass, please add it. Look at DTensor.__init__ implementation for example"
        )

    def wrapper(*args, **kwargs):
        constructor_subclass(*args, **kwargs)

        if not torch.compiler.is_exporting():
            return

        if not is_traceable_wrapper_subclass_type(type(args[0])):
            if not constructor_subclass.__qualname__.endswith("__init__"):
                raise AssertionError(
                    f"expected __qualname__ to end with '__init__', got {constructor_subclass.__qualname__}"
                )
            obj_name = constructor_subclass.__qualname__[: -len("__init__")]
            raise RuntimeError(
                f"Can't intercept {obj_name} in export because this object is not a traceable "
                f"tensor subclass. Please look at DTensor.__init__ implementation as an example of proper usage of this API."
            )

        mode = _maybe_find_pre_dispatch_tf_mode_for_export()
        if mode is None:
            return

        if not isinstance(mode, PreDispatchTorchFunctionMode):
            raise AssertionError(
                f"expected PreDispatchTorchFunctionMode, got {type(mode)}"
            )

        tracer = mode.tracer
        subclass = args[0]
        graphable = (tuple(args[1:]), kwargs)

        spec_name = "_".join(constructor_subclass.__qualname__.lower().split("."))
        call_spec_cache_key = type(subclass).__name__.lower()

        _emit_flat_apply_call(
            tracer=tracer,
            spec_name=spec_name,
            const_target_for_apply=type(subclass),
            graphable_args=graphable,
            track_value=subclass,  # track the constructed subclass instance
            call_spec_cache_key=call_spec_cache_key,
        )
        return

    return wrapper

