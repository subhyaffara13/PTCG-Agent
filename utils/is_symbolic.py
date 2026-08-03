from typing import Any

def is_symbolic(a: Any) -> TypeGuard[torch.SymInt | torch.Tensor]:
    return isinstance(a, torch.SymInt) or (
        isinstance(a, torch.Tensor) and a._has_symbolic_sizes_strides
    )


def is_symbolic(
    val: int | SymInt | float | SymFloat | bool | SymBool,
) -> TypeGuard[SymInt | SymFloat | SymBool]:
    if isinstance(val, (int, float, bool)):
        return False
    return val.node.is_symbolic()

