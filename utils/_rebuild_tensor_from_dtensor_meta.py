
def _rebuild_tensor_from_dtensor_meta(arg) -> object:
    """
    This is used to propagate tensor metadata, must be under fake mode
    """
    if arg.tensor_meta is None:
        raise AssertionError("DTensorSpec does not contain tensor_meta.")
    return torch.empty_strided(
        arg.tensor_meta.shape,
        arg.tensor_meta.stride,
        dtype=arg.tensor_meta.dtype,
    )

