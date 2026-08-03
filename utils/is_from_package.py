from typing import Any

def is_from_package(obj: Any) -> bool:
    """
    Return whether an object was loaded from a package.

    Note: packaged objects from externed modules will return ``False``.
    """
    if type(obj) is ModuleType:
        return is_mangled(obj.__name__)
    else:
        return is_mangled(type(obj).__module__)

