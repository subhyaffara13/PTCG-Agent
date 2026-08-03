from typing import Any, Dict

def _filter_einsum_defaults(kwargs: Dict[_EinsumDefaultKeys, Any]) -> Dict[_EinsumDefaultKeys, Any]:
    """Filters out default contract kwargs to pass to various backends."""
    kwargs = kwargs.copy()
    ret: Dict[_EinsumDefaultKeys, Any] = {}
    if (order := kwargs.pop("order", "K")) != "K":
        ret["order"] = order

    if (casting := kwargs.pop("casting", "safe")) != "safe":
        ret["casting"] = casting

    if (dtype := kwargs.pop("dtype", None)) is not None:
        ret["dtype"] = dtype

    if (out := kwargs.pop("out", None)) is not None:
        ret["out"] = out

    ret.update(kwargs)
    return ret

