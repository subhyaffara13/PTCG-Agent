
def _flatten_tensor_size(size) -> torch.Size:
    """
    Checks if tensor size is valid, then flatten/return a torch.Size object.
    """
    if len(size) == 1 and isinstance(size[0], collections.abc.Sequence):
        dims = list(*size)
    else:
        dims = list(size)

    for dim in dims:
        if not isinstance(dim, int):
            raise TypeError(f"size has to be a sequence of ints, found: {dims}")

    return torch.Size(dims)

