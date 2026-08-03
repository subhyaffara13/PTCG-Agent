from typing import Any

def _unsafe_set_version_counter_functional(
    ctx: AbstractContextManager[Any],
    tensors: tuple[torch.Tensor, ...],
    versions: tuple[int, ...],
) -> None:
    torch._C._autograd._unsafe_set_version_counter(tensors, versions)

