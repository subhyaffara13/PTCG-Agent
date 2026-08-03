import functools
from typing import Any, Callable

def _fn_html_repr(fn: Callable[..., Any]) -> str:
  """Constructs the signature representation of a function."""
  # TODO(epot): Special partial case (should likely be another custom node)
  if isinstance(fn, functools.partial):
    return _obj_html_repr(fn)

  try:
    # TODO(epot): When using built-in, should display `object.__repr__` rather
    # than `A.__repr__`
    fn_name = fn.__qualname__
  except Exception:  # pylint: disable=broad-except
    # Not sure when this could happen
    return _obj_html_repr(fn)

  # Do not add annotations/default in the one-line repr (would be too
  # boilerplate)

  sig_str = f'{fn_name}({_fn_signature_repr(fn)})'
  sig_str = _truncate_long_str(sig_str)
  return H.span(class_='fn')('ƒ') + ' ' + H.span(class_=['preview'])(sig_str)

