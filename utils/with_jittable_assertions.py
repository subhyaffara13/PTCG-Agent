from typing import Any, Callable

def with_jittable_assertions(fn: Callable[..., Any],
                             async_check: bool = True) -> Callable[..., Any]:
  """An alias for `chexify` (see the docs)."""
  return chexify(fn, async_check)

