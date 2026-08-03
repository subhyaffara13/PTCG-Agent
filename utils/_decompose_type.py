from typing import Union

def _decompose_type(t, to_list=True):
    if isinstance(t, TypeVar):
        if t.__bound__ is not None:
            ts = [t.__bound__]
        else:
            # For T_co, __constraints__ is ()
            ts = list(t.__constraints__)
    elif hasattr(t, "__origin__") and t.__origin__ == Union:
        ts = t.__args__
    else:
        if not to_list:
            return None
        ts = [t]
    # Ignored: Generator has incompatible item type "object"; expected "Type[Any]"
    ts = [TYPE2ABC.get(_t, _t) for _t in ts]  # type: ignore[misc]
    return ts

