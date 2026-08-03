from typing import Any

def var_impl(self: ComplexTensor, *args: Any, **kwargs: Any) -> torch.Tensor:
    self_re, self_im = split_complex_tensor(self)
    return torch.var(self_re, *args, **kwargs) + torch.var(self_im, *args, **kwargs)

