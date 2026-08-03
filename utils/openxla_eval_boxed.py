from typing import Any, Callable

def openxla_eval_boxed(
    model: fx.GraphModule, fake_tensor_inputs: list[torch.Tensor]
) -> Callable[..., Any]:
    return xla_backend_helper(model, fake_tensor_inputs, boxed=True)

