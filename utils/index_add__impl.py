from typing import Any

def index_add__impl(
    self: ComplexTensor,
    dim: int,
    index: torch.Tensor,
    source: ComplexTensor,
    **kwargs: Any,
) -> ComplexTensor:
    alpha = kwargs.pop("alpha", None)
    if alpha is not None:
        source = source * alpha

    self_re, self_im = split_complex_arg(self)
    source_re, source_im = split_complex_arg(source)

    ret_re = self_re.index_add_(dim, index, source_re)
    ret_im = self_im.index_add_(dim, index, source_im)

    return ComplexTensor(ret_re, ret_im)

