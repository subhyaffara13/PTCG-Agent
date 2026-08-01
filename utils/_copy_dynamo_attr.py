
def _copy_dynamo_attr(src: torch.Tensor, dst: torch.Tensor, attr: str) -> None:
    """Copy a single dynamo attribute from src to dst, or remove it from dst if src doesn't have it."""
    if hasattr(src, attr):
        setattr(dst, attr, getattr(src, attr).copy())
    elif hasattr(dst, attr):
        delattr(dst, attr)

