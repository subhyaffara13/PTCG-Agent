
def _qdd_cache_update(fun, in_type, i, consts, aval_qdds):
  cases = _seen_qdds_get(fun, in_type)
  if i == len(cases):
    cases.append([(c, aval_qdd.qdd) for c, aval_qdd in zip(consts, aval_qdds)
                  if aval_qdd.has_qdd])

