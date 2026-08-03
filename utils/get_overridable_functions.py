from typing import Any, Callable

def get_overridable_functions() -> dict[Any, list[Callable]]:
    """List functions that are overridable via __torch_function__

    Returns
    -------
    Dict[Any, List[Callable]]
        A dictionary that maps namespaces that contain overridable functions
        to functions in that namespace that can be overridden.
    """
    return _get_overridable_functions()[0]


def get_overridable_functions() -> set[Callable[..., Any]]:
    from itertools import chain

    from torch.overrides import get_overridable_functions as get_overridable_functions_
    from torch.utils._device import _device_constructors

    funcs = set(chain.from_iterable(get_overridable_functions_().values()))
    funcs.update(_device_constructors())
    more: set[Callable[..., Any]] = {
        torch.ones_like,
        torch.zeros_like,
        torch.empty_like,
        torch.full_like,
    }
    funcs.update(more)
    return funcs

