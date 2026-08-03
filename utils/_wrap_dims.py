from typing import Any

def _wrap_dims(dim: Any, ndim: int, keepdim: bool = False) -> list[DimEntry]:
    """Convert dimension specification to list of DimEntry objects."""
    de = _wrap_dim(dim, ndim, keepdim)
    result = []
    if not de.is_none():
        result.append(de)
    else:
        for d in dim:
            result.append(_wrap_dim(d, ndim, keepdim))
    return result

