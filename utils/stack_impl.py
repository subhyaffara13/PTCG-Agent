from typing import Any

def stack_impl(self: list[ComplexTensor], *args: Any, **kwargs: Any) -> ComplexTensor:
    re_im_tuples = [split_complex_arg(self_i) for self_i in self]
    u = torch.stack([c[0] for c in re_im_tuples], *args, **kwargs)
    v = torch.stack([c[1] for c in re_im_tuples], *args, **kwargs)
    return ComplexTensor(u, v)

