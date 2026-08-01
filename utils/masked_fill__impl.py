
def masked_fill__impl(
    self: ComplexTensor, mask: torch.Tensor, value: complex
) -> ComplexTensor:
    self_re, self_im = split_complex_arg(self)
    value_re, value_im = split_complex_arg(value)

    ret_re = self_re.masked_fill_(mask, value_re)
    ret_im = self_im.masked_fill_(mask, value_im)

    return ComplexTensor(ret_re, ret_im)

