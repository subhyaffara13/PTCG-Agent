from typing import Any

def convert_int_to_concrete_values(dim: Any) -> int | None:
    if dim is None:
        return None
    if not is_symbolic(dim):
        return dim
    else:
        assert isinstance(dim, torch.SymInt)
        return dim.node.maybe_as_int()

