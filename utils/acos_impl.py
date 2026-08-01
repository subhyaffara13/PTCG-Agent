
def acos_impl(self: ComplexTensor) -> ComplexTensor:
    _, y = split_complex_tensor(self)
    acosh_z = torch.acosh(self)
    if not isinstance(acosh_z, ComplexTensor):
        raise AssertionError(f"acosh_z must be a ComplexTensor, got {type(acosh_z)}")
    acosh_z_re, acosh_z_im = split_complex_tensor(acosh_z)
    sign_im = 2 * torch.signbit(y) - 1
    return ComplexTensor(torch.abs(acosh_z_im), sign_im * torch.abs(acosh_z_re))

