
def _encode_tensor(t: Tensor) -> EncodedTensor:
    """Encode a tensor's metadata into a JSON-serializable dict.

    Args:
        t: PyTorch tensor to encode

    Returns:
        Dict containing shape, stride, and dtype information
    """
    return EncodedTensor(
        shape=tuple(t.shape),
        stride=tuple(t.stride()),
        dtype=str(t.dtype),
    )

