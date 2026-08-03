from typing import Any

def set_curr_adhoc_kwargs(
    adhoc_kwargs: dict[str, Any],
    *,
    scope: Scope,
) -> Iterator[None]:
  """Set the current adhoc kwargs (accessed by `epy.lazy_imports()`)."""
  global _CURR_ADHOC_KWARGS
  try:
    _CURR_ADHOC_KWARGS = dict(adhoc_kwargs) | {'__scope__': scope}
    yield
  finally:
    _CURR_ADHOC_KWARGS = None

