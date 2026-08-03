from typing import Callable

def _override_sym_repr(
    override: Callable[["torch.types.PySymType"], str],
) -> Iterator[None]:
    tmp = CodeGen._sym_repr
    try:
        CodeGen._sym_repr = override
        yield
    finally:
        CodeGen._sym_repr = tmp

