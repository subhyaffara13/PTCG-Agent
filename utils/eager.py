from typing import Any, Callable

def eager(
    gm: torch.fx.GraphModule, fake_tensor_inputs: list[torch.Tensor], **kwargs: Any
) -> Callable[..., Any]:
    if kwargs:
        log.warning("eager backend ignoring extra kwargs %s", kwargs)

    if torch._functorch.config.force_autograd_cache:
        from torch._dynamo.aot_compile_types import GraphModuleSerializableCallable

        return GraphModuleSerializableCallable(gm)
    return gm.forward

