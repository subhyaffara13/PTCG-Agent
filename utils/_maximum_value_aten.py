
def _maximum_value_aten(dtype: torch.dtype):
    if dtype == torch.bool:
        return True
    elif dtype.is_complex or dtype.is_floating_point:
        return torch.finfo(dtype).max
    else:
        return torch.iinfo(dtype).max

