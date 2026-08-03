from typing import Any

def infer_dtype_from(val) -> tuple[DtypeObj, Any]:
    """
    Interpret the dtype from a scalar or array.

    Parameters
    ----------
    val : object
    """
    if not is_list_like(val):
        return infer_dtype_from_scalar(val)
    return infer_dtype_from_array(val)

