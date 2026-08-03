from typing import Any

def low_precision_fp_var(var: CSEVariable | Any) -> bool:
    if not isinstance(var, CSEVariable):
        return False

    dtype = var.dtype
    return low_precision_fp(dtype) if isinstance(dtype, torch.dtype) else False

