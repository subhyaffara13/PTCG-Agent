
def tanh_impl(self: ComplexTensor) -> ComplexTensor:
    x, y = split_complex_tensor(self)
    out_dt, (x, y) = promote_tensors(x, y)

    _2x = 2 * x
    _2y = 2 * y
    _d = torch.cosh(_2x) + torch.cos(_2y)
    _2xsh = torch.sinh(_2x)

    out_re = _2xsh / _d
    out_im = torch.sin(_2y) / _d

    return ComplexTensor(out_re.to(out_dt), out_im.to(out_dt))

