
def abs_impl(self: ComplexTensor) -> torch.Tensor:
    x, y = split_complex_tensor(self)
    out_dt, (x, y) = promote_tensors(x, y)
    result = torch.hypot(x, y)
    return result.to(out_dt)

