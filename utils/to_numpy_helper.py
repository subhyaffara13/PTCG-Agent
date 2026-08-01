
def to_numpy_helper(value: Any) -> Any:
    """Convert tensor and tnp.ndarray to numpy.ndarray."""
    if is_fake(value):
        return value
    if isinstance(value, tnp.ndarray):
        return to_numpy_helper(value.tensor)
    elif isinstance(value, torch.Tensor):
        return value.numpy(force=True)
    elif isinstance(value, (tuple, list)):
        return type(value)(to_numpy_helper(obj) for obj in value)
    else:
        return value

