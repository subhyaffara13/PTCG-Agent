from typing import Any

def iinfo(dtyp):
    torch_dtype = _dtypes.dtype(dtyp).torch_dtype
    return torch.iinfo(torch_dtype)


def iinfo(type_: DType | Array, /, xp: Namespace) -> Any:
    try:
        return xp.iinfo(type_)
    except (ValueError, TypeError):
        return xp.iinfo(type_.dtype)

