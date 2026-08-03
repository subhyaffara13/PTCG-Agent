from typing import Any, Callable

def _apply_func_to_inner_tensors_of_same_dim(
    func: Callable[..., Any], t: object, *args: Any, **kwargs: Any
) -> None:
    assert is_traceable_wrapper_subclass(t)

    attrs, _ctx = t.__tensor_flatten__()
    assert isinstance(t, torch.Tensor)
    for attr in attrs:
        match getattr(t, attr):
            case torch.Tensor() as inner:
                if inner.dim() == t.dim():
                    func(inner, *args, **kwargs)
            case OpaqueBase():
                pass
            case unexpected:
                raise AssertionError(
                    f"expected Tensor or OpaqueBase, got {type(unexpected)}"
                )

