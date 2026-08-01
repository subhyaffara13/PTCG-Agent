
def index_put_impl(
    fake_mode: FakeTensorMode, func: OpOverload, *args: Any, **kwargs: Any
) -> FakeTensor:
    _, new_kwargs = _normalize_function_or_error(
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )
    values = new_kwargs["values"]
    self_device = new_kwargs["input"].fake_device
    torch._check(
        self_device == values.fake_device or (values.ndim == 0 and values.numel() == 1),
        lambda: f"Mismatching {func} device between self ({self_device}) and values ({values.device})",
    )

    out = run_and_return_new_tensor_of_input_device(fake_mode, func, args, kwargs)
    if func is aten.index_put_.default:
        return new_kwargs["input"]
    else:
        return out

