
def _to_real_dtype(dtype):
    if dtype == torch.complex128:
        return torch.float64
    elif dtype == torch.complex64:
        return torch.float32
    else:
        return dtype

