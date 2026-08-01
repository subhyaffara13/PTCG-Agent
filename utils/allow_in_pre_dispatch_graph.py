
def allow_in_pre_dispatch_graph(func):
    """
    Experimental decorator that adds user function to export pre-dispatch graph. Note that
    we only support custom autograd function/subclass constructors today. To use this function:
        1. For subclasses:
            1. refer to instructions in mark_subclass_constructor_exportable_experimental
        2. Define apply method on your custom autograd function and apply this decorator.

    Example:

    class MyCoolCustomAutogradFunc(autograd.Function):
        @classmethod
        @torch._export.wrappers.allow_in_pre_dispatch_graph
        def apply(cls, *args, **kwargs):
            return super(MyCoolCustomAutogradFunc, cls).apply(*args, **kwargs)

    """
    if _is_init(func):
        return mark_subclass_constructor_exportable_experimental(func)

    if not (_is_init(func) or func.__name__ == "apply"):
        raise RuntimeError(
            f"torch._export.wrappers.allow_in_pre_dispatch_graph can only be applied on subclass tensor.__init_ "
            f"or custom_autograd_function.apply. "
            f"But, you are adding it on {func.__name__} which is not supported. "
            f"If __init__ doesn't exist on your subclass, please add it. Look at DTensor.__init__ implementation for example. "
            f"If you are adding it on custom autograd function, please add it on apply method. "
            f"If anything else, file an issue on github and we may consider extending our support. "
        )

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not torch.compiler.is_exporting():
            return func(*args, **kwargs)

        if not inspect.isclass(args[0]):
            return func(*args, **kwargs)

        if not issubclass(args[0], torch.autograd.Function):
            return func(*args, **kwargs)

        from torch._ops import _get_dispatch_mode_pre_dispatch

        mode = _get_dispatch_mode_pre_dispatch(torch._C._TorchDispatchModeKey.PROXY)
        if mode is None:
            return func(*args, **kwargs)

        # Sometimes custom autograd functions can call into HOPs that don't have proxy impl
        # at PreDispatch level, so we just dispatch it below to get the concrete result.
        include_to_set = torch._C._dispatch_tls_local_include_set().remove(
            torch._C.DispatchKey.PreDispatch
        )
        exclude_to_set = (
            torch._C._dispatch_tls_local_exclude_set()
            | torch._C.DispatchKeySet(torch._C.DispatchKey.PreDispatch)
        )

        with torch._C._ForceDispatchKeyGuard(include_to_set, exclude_to_set):
            out = func(*args, **kwargs)

        if not mode.pre_dispatch:
            raise AssertionError("Should only do this in predispatch")
        tracer = mode.tracer

        function_cls_name = f"{args[0].__module__}.{args[0].__qualname__}"
        graphable = ((function_cls_name, *args[1:]), kwargs)

        from torch.export.custom_ops import (
            _call_custom_autograd_function_in_pre_dispatch,
        )

        spec_name = "_".join(function_cls_name.split("."))
        call_spec_cache_key = type(
            _call_custom_autograd_function_in_pre_dispatch
        ).__name__.lower()
        _emit_flat_apply_call(
            tracer=tracer,
            spec_name=spec_name,
            const_target_for_apply=_call_custom_autograd_function_in_pre_dispatch,
            graphable_args=graphable,
            track_value=out,
            call_spec_cache_key=call_spec_cache_key,
        )
        return out

    return wrapper

