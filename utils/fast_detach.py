
def fast_detach(
    fake_mode: FakeTensorMode, x: FakeTensor, include_real: bool = False
) -> FakeTensor:
    with no_python_dispatcher(), in_kernel_invocation_manager(fake_mode):
        out = torch.ops.aten.detach.default(x)
    if include_real:
        return FakeTensor(fake_mode, out, x.device, real_tensor=x.real_tensor)
    return FakeTensor(fake_mode, out, x.device)

