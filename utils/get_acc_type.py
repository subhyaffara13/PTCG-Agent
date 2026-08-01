
def get_acc_type(dtype: torch.dtype, device: torch.device) -> torch.dtype:
    # Equivalent to at::toAccumulateType, prefer computation_dtype where possible
    if device.type == "cpu":
        return _cpu_acc_type_map.get(dtype, dtype)
    else:
        return get_computation_dtype(dtype)

