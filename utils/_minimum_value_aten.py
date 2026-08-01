
def _minimum_value_aten(dtype: torch.dtype):
    if dtype == torch.bool:
        return False
    elif dtype.is_complex or dtype.is_floating_point:
        return torch.finfo(dtype).min
    else:
        return torch.iinfo(dtype).min

