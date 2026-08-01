
def _reduce_jvp_rule(primals, tangents, *, computation, jaxpr, dimensions):
  primal_xs, init_values = split_list(primals, [len(primals) // 2])
  tangent_xs, tangent_init = split_list(tangents, [len(tangents) // 2])
  # This test may be too strict, if a value is actually zero but we cannot prove
  # it is symbolically zero.
  if any(type(t) is not ad_util.Zero for t in tangent_init):
    raise NotImplementedError(
      "Gradient of general lax.reduce with non-zero tangents for "
      "initial values to reduction not implemented")
  reducer = core.jaxpr_as_fun(jaxpr)
  return _reduce_jvp(reducer, init_values, primal_xs, tangent_xs, dimensions)

