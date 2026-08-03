import sys

def _issubclass_fast(cls: type, modname: str, clsname: str) -> bool:
    try:
        mod = sys.modules[modname]
    except KeyError:
        return False
    parent_cls = getattr(mod, clsname)
    return issubclass(cls, parent_cls)

