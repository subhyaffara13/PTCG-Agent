from typing import Any

def get_custom_getattr(
    value: Any, ignore_nn_module_getattr: bool = False
) -> Any | None:
    try:
        getattr_fn = inspect.getattr_static(type(value), "__getattr__")
    except AttributeError:
        getattr_fn = None
    if ignore_nn_module_getattr and getattr_fn is torch.nn.Module.__getattr__:
        # ignore this case of getattr
        getattr_fn = None
    return getattr_fn

