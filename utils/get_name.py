from typing import Union

def get_name() -> str:
    r"""Return Metal device name"""
    return torch._C._mps_get_name()


def get_name(x: Union[FuncBase, SymbolNode]) -> str:
    """
    Used for compatibility with mypy 0.740; can be dropped once support for 0.740 is dropped.
    """
    fn = x.name
    if callable(fn):  # pragma: no cover
        return fn()
    return fn

