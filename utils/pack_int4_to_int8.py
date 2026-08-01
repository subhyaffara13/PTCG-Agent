
def pack_int4_to_int8(weight):
    if weight.dim() != 2:
        raise AssertionError(f"weight must be 2D, got {weight.dim()}D")
    if weight.shape[1] % 2 != 0:
        raise AssertionError(f"weight.shape[1] must be even, got {weight.shape[1]}")
    if weight.dtype != torch.int8:
        raise AssertionError(f"weight.dtype must be int8, got {weight.dtype}")
    return ((weight[:, 1::2] & 0xF) << 4) | (weight[:, 0::2] & 0xF)

