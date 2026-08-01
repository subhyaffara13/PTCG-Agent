
def non_kwarg_to(
    fake_mode: FakeTensorMode, func: OpOverload, *args: Any, **kwargs: Any
) -> FakeTensor:
    _, new_kwargs = _normalize_function_or_error(
        func, args, kwargs, normalize_to_only_use_kwargs=True
    )
    input_device = new_kwargs["device"]
    out_device = input_device if input_device else new_kwargs["input"].device
    new_kwargs["device"] = torch.device("meta")
    inp = new_kwargs.pop("input")
    with in_kernel_invocation_manager(fake_mode):
        r = func(inp, **new_kwargs)
    # TODO: I think this does the wrong thing if r is inp
    return fake_mode.fake_tensor_converter.from_meta_and_device(
        fake_mode, r, out_device
    )

