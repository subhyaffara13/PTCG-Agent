from typing import Any

def _maybe_wrap_functional_tensor(
    maybe_tensor: Any, level: int, *, _python_functionalize: bool = False
) -> Any:
    if not isinstance(maybe_tensor, torch.Tensor):
        return maybe_tensor
    wrapped = _wrap_functional_tensor(maybe_tensor, level)
    _assert_wrapped_functional(maybe_tensor, wrapped)
    if _python_functionalize:
        # pyrefly: ignore[missing-argument]
        out = FunctionalTensor(wrapped)
        # pyrefly: ignore[missing-attribute]
        torch._mirror_autograd_meta_to(maybe_tensor, out)
        return out
    return wrapped

