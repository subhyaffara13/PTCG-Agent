
def _ref_jvp(primals, tangents, *, memory_space, kind):
  (init_val,), (init_dot,) = primals, tangents
  primal_out = core.ref_p.bind(init_val, memory_space=memory_space, kind=kind)
  if type(init_dot) is ad_util.Zero:
    zero = ad_util.zeros_like_aval(init_dot.aval)
    tangent_out = core.ref_p.bind(zero, memory_space=memory_space, kind=kind)
  else:
    tangent_out = core.ref_p.bind(init_dot, memory_space=memory_space, kind=kind)
  return primal_out, tangent_out

