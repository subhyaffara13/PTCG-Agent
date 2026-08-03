from typing import Any

def build_stream(args: tuple[Any], kwargs: dict[Any, Any]) -> torch.Stream:
    return torch._C.Stream(*args, **kwargs)

