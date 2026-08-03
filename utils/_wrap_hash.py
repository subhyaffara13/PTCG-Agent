import functools
from typing import Any, Callable

def _wrap_hash(hash_fn: Callable[..., Any]) -> Callable[..., Any]:
  """Wraps a hash function with some check for Flax Modules."""

  @functools.wraps(hash_fn)
  def wrapped(self):
    if self.scope is not None:
      raise TypeError("Can't call __hash__ on modules that hold variables.")
    try:
      hash_value = hash_fn(self)
    except TypeError as exc:
      raise TypeError(
        'Failed to hash Flax Module.  '
        'The module probably contains unhashable attributes.  '
        f'Module={self}'
      ) from exc
    return hash_value

  return wrapped

