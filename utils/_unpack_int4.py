
def _unpack_int4(packed: torch.Tensor, original_width: int) -> torch.Tensor:
    """Unpack int4 values from uint8 storage. Two values per byte.

    Each byte: low nibble = first value, high nibble = second value.
    Values are stored unsigned in [0, 15] and shifted to signed [-8, 7].
    Cast to uint8 first so the right shift is logical, not arithmetic.
    """
    packed = packed.to(torch.uint8)
    low = (packed & 0x0F).to(torch.int8) - 8
    high = (packed >> 4).to(torch.int8) - 8
    interleaved = torch.stack([low, high], dim=-1).reshape(*packed.shape[:-1], -1)
    return interleaved[..., :original_width]

