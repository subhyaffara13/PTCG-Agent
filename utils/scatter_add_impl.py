
def scatter_add_impl(
    self: ComplexTensor, dim: int, index: torch.Tensor, src: ComplexTensor
) -> ComplexTensor:
    self_re, self_im = split_complex_arg(self)
    src_re, src_im = split_complex_arg(src)

    ret_re = torch.scatter_add(self_re, dim, index, src_re)
    ret_im = torch.scatter_add(self_im, dim, index, src_im)

    return ComplexTensor(ret_re, ret_im)

