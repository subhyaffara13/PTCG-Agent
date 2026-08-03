import functools
from typing import Any

def randint_like_low(
    self: torch.Tensor, low: int, high: int, **kwargs: Any
) -> torch.Tensor:
    return _rand_like(functools.partial(aten.randint.low, low, high), self, **kwargs)

