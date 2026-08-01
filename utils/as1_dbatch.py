
def as1Dbatch(tensor):
    """Return tensor as 3D tensor by either prepending new dimensions to
    the tensor shape (when ``tensor.ndim < 3``), or by collapsing
    starting dimensions into the first dimension (when ``tensor.ndim >
    3``).
    """
    while tensor.ndim < 3:
        tensor = tensor.unsqueeze(0)
    if tensor.ndim > 3:
        tensor = tensor.flatten(0, tensor.ndim - 3)
    if tensor.ndim != 3:
        raise AssertionError(
            f"tensor should have 3 dimensions after reshape, got {tensor.shape}"
        )
    return tensor

