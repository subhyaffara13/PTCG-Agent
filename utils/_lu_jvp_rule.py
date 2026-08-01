
def _lu_jvp_rule(primals, tangents):
  a, = primals
  a_dot, = tangents
  lu, pivots, permutation = lu_p.bind(a)

  lu_dot_fun = _lu_jvp_inner
  for _ in np.shape(a)[:-2]:
    lu_dot_fun = api.vmap(lu_dot_fun)
  lu_dot = lu_dot_fun(lu, a_dot, permutation)

  return (lu, pivots, permutation), (lu_dot, ad_util.p2tz(pivots),
                                     ad_util.p2tz(permutation))

