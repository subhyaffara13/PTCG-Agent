
def run_and_return_new_tensor_of_input_device(
    fake_mode: FakeTensorMode,
    func: OpOverload,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> FakeTensor:
    # TODO: ref
    _, new_kwargs = _normalize_function_or_error(
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )
    out_device = new_kwargs["input"].device
    with in_kernel_invocation_manager(fake_mode):
        out = func(*args, **kwargs)
        if not is_noncontiguous_supported(out_device):
            out = out.new_empty(out.shape)

    if out is new_kwargs["input"]:
        return out  # copy_
    return FakeTensor(fake_mode, out, out_device)

