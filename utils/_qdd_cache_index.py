
def _qdd_cache_index(fun, in_type) -> int:
  cases = _seen_qdds_get(fun, in_type)
  for i, records in enumerate(cases):
    for obj, qdd in records:
      if core.cur_qdd(obj) != qdd: break
    else:
      return i
  return len(cases)

