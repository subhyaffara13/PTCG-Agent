from typing import Any

def ne_impl(
    self: ComplexTensor, rhs: ComplexTensor, *args: Any, **kwargs: Any
) -> torch.Tensor:
    a_r, a_i = split_complex_tensor(self)
    b_r, b_i = split_complex_arg(rhs)
    return torch.ne(a_r, b_r, *args, **kwargs) | torch.ne(a_i, b_i, *args, **kwargs)

