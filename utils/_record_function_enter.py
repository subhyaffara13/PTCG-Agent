
def _record_function_enter(
    fake_mode: FakeTensorMode, func: OpOverload, name: str, args: object | None = None
) -> FakeTensor:
    # Call the real implementation to get a real handle tensor
    with in_kernel_invocation_manager(fake_mode):
        real_handle = func(name, args)
    # Create a meta tensor with the same properties as the real handle
    meta_handle = torch.empty_like(real_handle, device="meta")
    # Wrap it as a FakeTensor
    return FakeTensor(fake_mode, meta_handle, torch.device("cpu"))

