from typing import Any, Callable

def dummy_fx_compile(
    gm: fx.GraphModule, example_inputs: list[torch.Tensor]
) -> Callable[..., Any]:
    return gm.forward

