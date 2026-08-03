import os
from typing import Callable

def _auto_chmod(
    func: Callable[..., _T], arg: str, exc: BaseException
) -> _T:  # pragma: no cover
    """shutils onexc callback to automatically call chmod for certain functions."""
    # Only retry for scenarios known to have an issue
    if func in [os.unlink, os.remove] and os.name == 'nt':
        attempt_chmod_verbose(arg, stat.S_IWRITE)
        return func(arg)
    raise exc

