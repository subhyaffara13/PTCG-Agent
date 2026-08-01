
def low_prec_float(dtype: torch.dtype) -> bool:
    return dtype.is_floating_point and dtype.itemsize < 4

