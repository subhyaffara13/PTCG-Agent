import functools
from typing import Any, Callable

def resolve_kwargs(fun: Callable, args, kwargs) -> tuple[Any, ...]:
  """Resolve input arguments to positional following a function's signature.

  This will raise a TypeError if any keyword-only arguments were passed by the
  caller.
  """
  if isinstance(fun, partial):
    # functools.partial should have an opaque signature.
    fun = lambda *args, **kwargs: None
  ba = inspect.signature(fun).bind(*args, **kwargs)
  ba.apply_defaults()
  if ba.kwargs:
    passed_kwargs = [k for k in ba.kwargs if k in kwargs]
    if passed_kwargs:
      raise TypeError(
          "The following keyword arguments could not be resolved to positions: "
          f"{', '.join(passed_kwargs)}"
      )
  return ba.args


def resolve_kwargs(
  fun: tp.Callable[..., tp.Any],
  args: tuple,
  kwargs: dict[str, tp.Any],
) -> tuple: ...


def resolve_kwargs() -> tp.Callable[[F], F]: ...


def resolve_kwargs(
  fun: tp.Callable[..., tp.Any] | Missing = MISSING,
  args: tuple | Missing = MISSING,
  kwargs: dict[str, tp.Any] | Missing = MISSING,
) -> tuple | tp.Callable[[F], F]:
  if isinstance(fun, Missing):

    def resolve_kwargs_decorator(f):
      @functools.wraps(f)
      def resolve_kwargs_wrapper(*args, **kwargs):
        args = resolve_kwargs(f, args, kwargs)
        return f(*args)

      return resolve_kwargs_wrapper

    return resolve_kwargs_decorator  # type: ignore

  if isinstance(args, Missing):
    raise ValueError('args must be provided')
  if isinstance(kwargs, Missing):
    raise ValueError('kwargs must be provided')

  if isinstance(fun, functools.partial):
    # functools.partial should have an opaque signature.
    fun = lambda *args, **kwargs: None
  ba = inspect.signature(fun).bind(*args, **kwargs)
  ba.apply_defaults()
  if ba.kwargs:
    raise TypeError('keyword arguments could not be resolved to positions')
  else:
    return ba.args

