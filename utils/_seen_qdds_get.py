
def _seen_qdds_get(fun, in_type) -> list:
  cache = _seen_qdds.setdefault(fun, defaultdict(list))
  assert cache is not None  # pyrefly#2407
  return cache[in_type]

