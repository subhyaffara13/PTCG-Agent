from typing import Callable

def _make_deprecate(meth: Callable[_P, _R]) -> Callable[_P, _R]:
    new_name = meth.__name__
    old_name = new_name[:-1]

    def deprecated_init(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        warnings.warn(
            f"`nn.init.{old_name}` is now deprecated in favor of `nn.init.{new_name}`.",
            FutureWarning,
            stacklevel=2,
        )
        return meth(*args, **kwargs)

    deprecated_init.__doc__ = rf"""
    {old_name}(...)

    .. warning::
        This method is now deprecated in favor of :func:`torch.nn.init.{new_name}`.

    See :func:`~torch.nn.init.{new_name}` for details."""
    deprecated_init.__name__ = old_name
    return deprecated_init

