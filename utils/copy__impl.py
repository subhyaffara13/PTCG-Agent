from typing import Any

def copy__impl(
    self: ComplexTensor | torch.Tensor,
    src: ComplexTensor | torch.Tensor,
    *args: Any,
    **kwargs: Any,
) -> ComplexTensor | torch.Tensor:
    if not self.dtype.is_complex:
        warnings.warn(
            "Casting complex values to real discards the imaginary part", UserWarning
        )
        src_re, src_im = split_complex_arg(src)
        return self.copy_(src_re)

    self_re, self_im = split_complex_arg(self)
    src_re, src_im = split_complex_arg(src)

    ret_re = self_re.copy_(src_re, *args, **kwargs)
    ret_im = self_im.copy_(src_im, *args, **kwargs)

    return ComplexTensor(ret_re, ret_im)

