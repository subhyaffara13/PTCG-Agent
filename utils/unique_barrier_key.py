from typing import Optional

def unique_barrier_key(
    key: str,
    *,
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
) -> str:
  """Constructs a key given an optional prefix and suffix."""
  if prefix is not None:
    key = f'{prefix}_{key}'
  if suffix is not None:
    key = f'{key}.{suffix}'
  return key


def unique_barrier_key(
    key: str,
    *,
    prefix: str | None = None,
    suffix: str | None = None,
) -> str:
  """Constructs a key given an optional prefix and suffix."""
  if prefix is not None:
    key = f'{prefix}_{key}'
  if suffix is not None:
    key = f'{key}.{suffix}'
  return key

