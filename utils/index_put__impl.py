
def index_put__impl(
    self: ComplexTensor,
    indices: tuple[torch.Tensor, ...],
    values: ComplexTensor,
    accumulate: bool = False,
) -> ComplexTensor:
    self_re, self_im = split_complex_arg(self)
    values_re, values_im = split_complex_arg(values)

    out_re = self_re.index_put_(indices, values_re, accumulate=accumulate)
    out_im = self_im.index_put_(indices, values_im, accumulate=accumulate)

    return ComplexTensor(out_re, out_im)

