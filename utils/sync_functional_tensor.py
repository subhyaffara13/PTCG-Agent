
def sync_functional_tensor(t: torch.Tensor) -> None:
    if is_traceable_wrapper_subclass(t):
        attrs, _ctx = t.__tensor_flatten__()  # type: ignore[attr-defined]
        for attr in attrs:
            match getattr(t, attr):
                case Tensor() as inner:
                    sync_functional_tensor(inner)
                case OpaqueBase():
                    pass
                case unexpected:
                    raise AssertionError(
                        f"expected Tensor or OpaqueBase, got {type(unexpected)}"
                    )
    else:
        torch._sync(t)

