from typing import Any

def _wrap_kwargs_hashable(kwargs: dict[str, Any]) -> Sequence[tuple[str, Any]]:
  hashable_kwargs: list[tuple[str, Any]] = []
  for k, v in sorted(kwargs.items()):
    if isinstance(v, np.ndarray):
      hashable_kwargs.append((k, HashableArray(v)))
    elif isinstance(v, dict):
      hashable_kwargs.append((k, FrozenDict(v)))
    else:
      try:
        hash(v)
      except TypeError as e:
        raise TypeError(
            f"Non-hashable keyword argument to ffi_call {k}: {v}") from e
      else:
        hashable_kwargs.append((k, v))
  return tuple(hashable_kwargs)

