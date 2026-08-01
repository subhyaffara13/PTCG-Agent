
def unpack_int8_to_int4(weight):
    if weight.dim() != 2:
        raise AssertionError(f"weight must be 2D, got {weight.dim()}D")
    if weight.dtype != torch.int8:
        raise AssertionError(f"weight.dtype must be int8, got {weight.dtype}")
    return torch.stack((weight & 0xF, (weight >> 4) & 0xF), dim=2).view(
        weight.shape[0], 2 * weight.shape[1]
    )

