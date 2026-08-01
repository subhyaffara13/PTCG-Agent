
def _create_flat_tensor_from_bytes(
    tensor_bytes: bytes,
    tensor_meta: schema.TensorMeta,
) -> torch.Tensor:
    """
    Create a flat tensor from raw bytes with dtype, device and requires_grad.
    It will be re-strided based on size, stride, and storage_offset later.
    """
    dtype = deserialize_scalar_type(tensor_meta.dtype)
    size = deserialize_size(tensor_meta.sizes)
    device = deserialize_device(tensor_meta.device)

    if len(tensor_bytes) != 0:
        tensor = torch.frombuffer(
            tensor_bytes, dtype=dtype, requires_grad=tensor_meta.requires_grad
        ).to(device)
    else:
        # cannot call torch.frombuffer() on empty bytes
        logger.warning(
            "Cannot call torch.frombuffer() on empty bytes. "
            "Creating a tensor with zeros as workaround."
        )
        tensor = torch.zeros(size, dtype=dtype, device=device)

    return tensor

