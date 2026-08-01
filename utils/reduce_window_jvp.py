
def reduce_window_jvp(
    primals,
    tangents,
    window_dimensions,
    window_strides,
    padding,
    base_dilation,
    window_dilation,
    jaxpr,
    consts,
):

  reduction_jaxpr = jaxpr

  n = len(primals) // 2  # number of primal operands
  operand, init_value = util.split_list(primals, [n])
  operand_tangent, init_value_tangent = util.split_list(tangents, [n])
  if not all(isinstance(t, ad.Zero) for t in init_value_tangent):
    raise TypeError("reduce_window jvp does not support non-zero init_value_tangent.")

  init_value_tangent = map(ad_util.instantiate, init_value_tangent)
  c_reduction_jaxpr = ClosedJaxpr(reduction_jaxpr, consts)
  jvp_reduction = ad.jvp_jaxpr(c_reduction_jaxpr, (True,) * len(tangents), [False] * len(init_value_tangent))[0]

  def wrapper(left, right):
    pl, tl = util.split_list(left, [n])
    pr, tr = util.split_list(right, [n])
    return jaxpr_as_fun(jvp_reduction)(*pl, *pr, *tl, *tr)

  jvp_primals_tangents = _reduce_window(
      operand=[*operand, *operand_tangent],
      init_value=[*init_value, *init_value_tangent],
      computation=wrapper,
      window_dimensions=window_dimensions,
      window_strides=window_strides,
      padding=padding,
      base_dilation=base_dilation,
      window_dilation=window_dilation,
  )
  primals, tangents = util.split_list(jvp_primals_tangents, [len(jvp_primals_tangents) // 2])
  return [*primals], [*tangents]

