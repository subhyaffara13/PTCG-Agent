
def supported_builtin_dtype_torch_dtype() -> dict[type, torch.dtype]:
    return {int: torch.int32, float: torch.float, bool: torch.bool}

