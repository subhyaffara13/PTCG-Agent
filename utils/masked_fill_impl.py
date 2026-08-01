
def masked_fill_impl(
    self: ComplexTensor, mask: torch.Tensor, value: complex
) -> ComplexTensor:
    self_re, self_im = split_complex_arg(self)
    value_re, value_im = split_complex_arg(value)

    ret_re = self_re.masked_fill(mask, value_re)
    ret_im = self_im.masked_fill(mask, value_im)

    return ComplexTensor(ret_re, ret_im)

