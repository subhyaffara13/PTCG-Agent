
def constant_pad_nd_impl(
    self: ComplexTensor, pad: Sequence[int], value: complex | None = None
) -> ComplexTensor:
    self_re, self_im = split_complex_tensor(self)
    if value is None:
        ret_re = aten.constant_pad_nd(self_re, pad)
        ret_im = aten.constant_pad_nd(self_im, pad)
    else:
        value_re, value_im = split_complex_arg(value)
        ret_re = aten.constant_pad_nd(self_re, pad, value_re)
        ret_im = aten.constant_pad_nd(self_im, pad, value_im)

    return ComplexTensor(ret_re, ret_im)

