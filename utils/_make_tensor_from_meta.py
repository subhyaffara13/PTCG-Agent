
def _make_tensor_from_meta(
    meta: _TensorMeta,
    device: torch.device | str,
) -> torch.Tensor:
    """Create a tensor from metadata.

    Args:
        meta: Metadata with shape, stride, and dtype.
        device: Target device for the tensor.

    Returns:
        Empty tensor preserving the exact memory layout.
    """
    return torch.empty_strided(
        size=meta.shape,
        stride=meta.stride,
        dtype=meta.dtype,
        device=device,
    )

