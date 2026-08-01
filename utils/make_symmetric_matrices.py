
def make_symmetric_matrices(*shape, device, dtype):
    if shape[-1] != shape[-2]:
        raise AssertionError(f"expected square matrix, got shape[-1]={shape[-1]} != shape[-2]={shape[-2]}")
    t = make_tensor(shape, device=device, dtype=dtype)
    t = (t + t.mT).div_(2)
    return t

