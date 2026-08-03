import re

def isinf_impl(self: ComplexTensor) -> torch.Tensor:
    re, im = split_complex_tensor(self)
    return torch.isinf(re) | torch.isinf(im)

