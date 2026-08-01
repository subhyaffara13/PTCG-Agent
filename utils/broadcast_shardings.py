
def broadcast_shardings(*avals):
  fst, *rst = avals
  if not rst:
    return fst.sharding

  # First check if we need only rank promotion (and not singleton-broadcasting).
  res_aval = _max(avals, key=lambda a: a.ndim)
  ndim = res_aval.ndim
  if ndim == 0 or all(
      P(*res_aval.sharding.spec[ndim - a.ndim:]) == a.sharding.spec
      for a in avals):
    return res_aval.sharding

  # Next try singleton-broadcasting, padding out ranks using singletons.
  aval_list = []
  for a in avals:
    new_spec = P(*(None,) * (ndim - a.ndim) + a.sharding.spec)
    new_shape = (1,) * (ndim - a.ndim) + a.shape
    aval_list.append(a.update(shape=new_shape,
                              sharding=a.sharding.update(spec=new_spec)))
  return broadcasting_sharding_rule('broadcast_shardings', *aval_list)

