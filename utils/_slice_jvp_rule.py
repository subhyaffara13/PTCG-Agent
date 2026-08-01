
def _slice_jvp_rule(primals, tangents, *, start_indices, limit_indices, strides):
  (p,), (t,) = primals, tangents
  primal_out = slice_p.bind(p, start_indices=start_indices,
                            limit_indices=limit_indices, strides=strides)
  if type(t) is ad.Zero:
    return primal_out, ad.p2tz(primal_out)
  else:
    tangent_out = slice_p.bind(t, start_indices=start_indices,
                               limit_indices=limit_indices, strides=strides)
    return primal_out, tangent_out

