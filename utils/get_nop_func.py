import functools
from typing import Any, Callable

def get_nop_func() -> Callable[
    [torch.fx.GraphModule, list[torch.Tensor]], Callable[..., Any]
]:
    if not torch._functorch.config.fake_tensor_crossref:
        return boxed_nop
    elif torch._functorch.config.fake_tensor_crossref == "all":
        return fake_crossref_boxed_nop
    else:
        assert torch._functorch.config.fake_tensor_crossref == "custom_ops"
        return functools.partial(fake_crossref_boxed_nop, ignore_op_fn=ignore_builtins)

