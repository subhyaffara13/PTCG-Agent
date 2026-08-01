
def _get_raw_tensor_bytes(value: torch.Tensor) -> bytes:
    """
    Get the raw bytes of a tensor. This is used to save the tensor in pt2 archive.
    """
    # NOTE: don't chain .cpu() with .data_ptr(). If an HtoD copy needs to be
    # performed, the CPU copy needs to be kept alive when its underlying
    # memory is accessed.
    import ctypes

    if _is_fake_tensor(value):
        value_bytes = b""
    elif value.data_ptr():
        cpu_tensor = value.cpu()
        value_untyped_storage = cpu_tensor.untyped_storage()
        # we store the raw bytes the untyped storage. Tensor metadata is stored separately
        value_bytes = bytes(
            ctypes.cast(
                value_untyped_storage.data_ptr(),
                ctypes.POINTER(ctypes.c_ubyte * value_untyped_storage.size()),
            ).contents
        )
    else:
        # for empty tensor
        value_bytes = b""
    return value_bytes

