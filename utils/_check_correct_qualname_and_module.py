import functools
import sys

def _check_correct_qualname_and_module(obj) -> bool:
    qualname = obj.__qualname__
    name = obj.__name__
    module_name = obj.__module__
    assert name == qualname.split(".")[-1]

    module = sys.modules[module_name]
    actual_obj = functools.reduce(getattr, qualname.split("."), module)
    return (
        actual_obj is obj or
        # `obj` may be a bound method/property of `actual_obj`:
        (
            hasattr(actual_obj, "__get__") and hasattr(obj, "__self__") and
            actual_obj.__module__ == obj.__module__ and
            actual_obj.__qualname__ == qualname
        )
    )

