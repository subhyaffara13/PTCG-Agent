
def multi_device_op_out(
    fake_mode: FakeTensorMode, func: OpOverload, *args: Any, **kwargs: Any
) -> FakeTensor:
    with in_kernel_invocation_manager(fake_mode):
        func(*args, **kwargs)

    _, new_kwargs = _normalize_function_or_error(
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    return new_kwargs["input"]

