
def _sub_jvp(primals, tangents):
  x, y = primals
  xdot, ydot = tangents
  primal_out = sub(x, y)
  if type(xdot) is type(ydot) is ad_util.Zero:
    return primal_out, ad_util.p2tz(primal_out)
  if type(xdot) is ad_util.Zero:
    return (primal_out, _maybe_broadcast(primal_out.shape, neg(ydot),
                                         typeof(primal_out).sharding))
  elif type(ydot) is ad_util.Zero:
    return (primal_out, _maybe_broadcast(primal_out.shape, xdot,
                                         typeof(primal_out).sharding))
  else:
    return primal_out, sub(xdot, ydot)

