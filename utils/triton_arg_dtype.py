from typing import Any

def triton_arg_dtype(arg: Any) -> torch.dtype | None:
    if isinstance(arg, CSEVariable):
        return arg.dtype
    if isinstance(arg, torch._prims_common.Number):
        return type_to_dtype(type(arg))
    return None

