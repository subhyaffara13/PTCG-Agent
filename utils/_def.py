from typing import Any

def _def(name: str, *args: Any, **kwargs: Any) -> None:
    orig = getattr(torch.Tensor, name)
    setattr(_Tensor, name, _wrap(orig, *args, **kwargs))

