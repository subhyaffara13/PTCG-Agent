
def _access_subclass_inner_tensor(
    src_subclass_tensor: torch.Tensor, attr: str
) -> torch.Tensor:
    from torch.utils._python_dispatch import is_traceable_wrapper_subclass

    if not is_traceable_wrapper_subclass(src_subclass_tensor):
        raise AssertionError(
            f"Expected src_subclass_tensor to be a traceable wrapper subclass, "
            f"but got {type(src_subclass_tensor)}"
        )
    val = getattr(src_subclass_tensor, attr, None)
    if val is None or not isinstance(val, torch.Tensor):
        raise RuntimeError(
            f"Attribute {attr} is not a tensor or doesn't exist in {src_subclass_tensor}"
        )
    return val

