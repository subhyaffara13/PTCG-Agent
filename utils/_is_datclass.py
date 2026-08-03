from typing import Any

def _is_datclass(obj: Any, *, force: bool = False) -> bool:
  """Returns `True` if the object is a dataclass."""
  if isinstance(obj, type):  # Class are not pretty-print
    return False
  if not dataclasses.is_dataclass(obj):
    return False
  if force:  # Force pretty-print even if custom `__repr__`
    return True
  if not obj.__dataclass_params__.repr:  # dataclass(repr=False)
    return False
  # TODO(epot): Better support for recursive `pretty_repr` to avoid infinite
  # loops.
  if has_default_repr(type(obj)) or type(obj).__repr__ in (
      pretty_repr,
      pretty_repr_top_level,
  ):
    return True
  return False

