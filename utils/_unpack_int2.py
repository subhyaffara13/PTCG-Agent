
def _unpack_int2(packed: torch.Tensor, original_width: int) -> torch.Tensor:
    """Unpack int2 values from uint8 storage. Four values per byte.

    Bits [1:0]/[3:2]/[5:4]/[7:6] hold values 0..3 each, shifted to signed [-2, 1].
    """
    packed = packed.to(torch.uint8)
    v0 = (packed & 0x03).to(torch.int8) - 2
    v1 = ((packed >> 2) & 0x03).to(torch.int8) - 2
    v2 = ((packed >> 4) & 0x03).to(torch.int8) - 2
    v3 = (packed >> 6).to(torch.int8) - 2
    interleaved = torch.stack([v0, v1, v2, v3], dim=-1).reshape(*packed.shape[:-1], -1)
    return interleaved[..., :original_width]

