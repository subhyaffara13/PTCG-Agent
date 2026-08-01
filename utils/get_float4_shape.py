
def get_float4_shape(tensor: torch.Tensor) -> tuple[int, ...]:
    """Get the shape of an unpacked float4 tensor.

    The float4_e2m1fn_x2 type is a shell type described in
    https://github.com/pytorch/pytorch/issues/146414.

    the shell dtype is takes up 1 byte per element and semantically represents
    two fp4 values packed into 1 byte. Semantically it represents (*tensor.shape[:-1], tensor.shape[-1]*2)
    fp4 elements.
    """
    if tensor.dtype != torch.float4_e2m1fn_x2:
        raise AssertionError(f"Expected float4_e2m1fn_x2, got {tensor.dtype}")
    return (*tensor.shape[:-1], tensor.shape[-1] * 2)

