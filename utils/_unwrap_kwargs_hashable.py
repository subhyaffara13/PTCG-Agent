
def _unwrap_kwargs_hashable(kwargs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
  unwrapped_kwargs: dict[str, Any] = {}
  for k, v in kwargs:
    if isinstance(v, HashableArray):
      unwrapped_kwargs[k] = v.val
    elif isinstance(v, FrozenDict):
      unwrapped_kwargs[k] = v._d
    else:
      unwrapped_kwargs[k] = v
  return unwrapped_kwargs

