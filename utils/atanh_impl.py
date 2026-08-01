
def atanh_impl(self: ComplexTensor) -> ComplexTensor:
    x, y = split_complex_tensor(self)
    out_dt, (x, y) = promote_tensors(x, y)

    ret = 0.5 * (
        torch.log(ComplexTensor(1 + x, y)) - torch.log(ComplexTensor(1 - x, -y))
    )
    if not isinstance(ret, ComplexTensor):
        raise AssertionError(f"ret must be a ComplexTensor, got {type(ret)}")
    ret_re, ret_im = split_complex_tensor(ret)

    return ComplexTensor(ret_re.to(out_dt), ret_im.to(out_dt))

