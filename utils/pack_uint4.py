
def pack_uint4(uint8_data) -> torch.Tensor:
    # converting to uint8 for operations
    shape = uint8_data.shape
    if shape[-1] % 2 != 0:
        raise AssertionError(f"Expected shape[-1] to be divisible by 2, got {shape[-1]}")
    uint8_data = uint8_data.contiguous().view(-1)
    return (uint8_data[1::2] << 4 | uint8_data[::2]).view(down_size(shape))

