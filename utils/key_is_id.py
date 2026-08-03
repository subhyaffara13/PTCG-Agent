from typing import Any

def key_is_id(
    k: Any,
) -> TypeIs[torch.Tensor | torch.nn.Module | MethodWrapperType]:
    """Returns whether it indexes dictionaries using its id"""
    return isinstance(k, (torch.Tensor, torch.nn.Module, MethodWrapperType))

