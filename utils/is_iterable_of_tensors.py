from typing import Any

def is_iterable_of_tensors(iterable: Iterable[Any]) -> bool:
    # Tensor itself is iterable so we check this first
    if isinstance(iterable, torch.Tensor):
        return False
    try:
        # pyrefly: ignore[bad-argument-type]
        if len(iterable) == 0:
            return False
        for t in iter(iterable):
            if not isinstance(t, torch.Tensor):
                return False
    except TypeError:
        return False
    return True


def is_iterable_of_tensors(iterable, include_empty=False):
    """ Returns True if iterable is an iterable of tensors and False o.w.

        If the iterable is empty, the return value is :attr:`include_empty`
    """
    # Tensor itself is iterable so we check this first
    if isinstance(iterable, torch.Tensor):
        return False

    try:
        if len(iterable) == 0:
            return include_empty

        for t in iter(iterable):
            if not isinstance(t, torch.Tensor):
                return False

    except TypeError:
        return False

    return True

