
def sqrt_impl(self: ComplexTensor) -> ComplexTensor:
    self_r, self_i = split_complex_tensor(self)
    out_dt, (self_r, self_i) = promote_tensors(self_r, self_i)
    self = ComplexTensor(self_r, self_i)
    self_abs_sqrt = torch.sqrt(torch.abs(self))
    self_half_angle = 0.5 * torch.angle(self)

    ret_r = self_abs_sqrt * torch.cos(self_half_angle)
    ret_i = self_abs_sqrt * torch.sin(self_half_angle)

    return ComplexTensor(ret_r.to(out_dt), ret_i.to(out_dt))

