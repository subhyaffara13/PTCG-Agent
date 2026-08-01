
def scatter_add__impl(
    self: ComplexTensor, dim: int, index: torch.Tensor, src: ComplexTensor
) -> ComplexTensor:
    self_re, self_im = split_complex_arg(self)
    src_re, src_im = split_complex_arg(src)

    out_re = self_re.scatter_add_(dim, index, src_re)
    out_im = self_im.scatter_add_(dim, index, src_im)

    return ComplexTensor(out_re, out_im)

