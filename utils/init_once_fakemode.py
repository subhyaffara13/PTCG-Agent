
def init_once_fakemode(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Wrapper around lazy init functions in fx_passes/"""

    _fn_params = inspect.signature(fn).parameters

    @functools.cache
    @functools.wraps(fn)
    def lazy_init(
        input_device: Any | None = None,
        get_decomp_fn: Callable[
            ..., dict[Any, Callable[..., Any]]
        ] = select_decomp_table,
    ) -> Any:
        counters_ref = counters[backend].copy()

        kwargs: dict[str, Any] = {}
        if "input_device" in _fn_params:
            kwargs["input_device"] = input_device
        if "get_decomp_fn" in _fn_params:
            kwargs["get_decomp_fn"] = get_decomp_fn

        with torch._guards.tracing(None), unset_fake_temporarily(), FakeTensorMode():
            result = fn(**kwargs)

        # clear view matches encountered during tracing
        counters[backend] = counters_ref

        return result

    return lazy_init

