
def pack_weights(quantized_weights: torch.Tensor) -> torch.Tensor:
    """
    Packs a tensor of quantized weights into a compact format using 2 bits per value.

    Parameters:
    -----------
    quantized_weights : torch.Tensor
        A tensor containing ternary quantized weights with values in {-1, 0, 1}. These values are adjusted to
        {0, 1, 2} before being packed.

    Returns:
    --------
    torch.Tensor
        A packed tensor where each element stores 4 quantized values (each using 2 bits) in an 8-bit format.
    """

    original_shape = quantized_weights.shape

    row_dim = (original_shape[0] + VALUES_PER_ITEM - 1) // VALUES_PER_ITEM

    if len(original_shape) == 1:
        packed_tensor_shape = (row_dim,)
    else:
        packed_tensor_shape = (row_dim, *original_shape[1:])

    quantized_weights += 1
    packed = torch.zeros(packed_tensor_shape, device=quantized_weights.device, dtype=torch.uint8)
    unpacked = quantized_weights.to(torch.uint8)

    it = min(VALUES_PER_ITEM, (original_shape[0] // row_dim) + 1)
    for i in range(it):
        start = i * row_dim
        end = min(start + row_dim, original_shape[0])
        packed[: (end - start)] |= unpacked[start:end] << 2 * i

    return packed

