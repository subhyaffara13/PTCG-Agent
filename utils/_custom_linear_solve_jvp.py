
def _custom_linear_solve_jvp(primals, tangents, const_lengths, jaxprs):
  # A x - b = 0
  # ∂A x + A ∂x - ∂b = 0
  # ∂x = A^{-1} (∂b - ∂A x)

  kwargs = dict(const_lengths=const_lengths, jaxprs=jaxprs)
  x = linear_solve_p.bind(*primals, **kwargs)

  params, _ = _split_linear_solve_args(primals, const_lengths)
  params_dot, b_dot = _split_linear_solve_args(tangents, const_lengths)

  num_x_leaves = len(b_dot)
  # x is a flat tree with possible aux values appended
  # since x_tree == b_tree == b_dot_tree, we can cut off
  # aux values with len info provided by b_dot tree here
  x_leaves, _ = split_list(x, [num_x_leaves])

  if all(type(p) is ad_util.Zero for p in params_dot.matvec):
    # no need to evaluate matvec_tangents
    rhs = b_dot
  else:
    matvec_tangents = _tangent_linear_map(
        core.jaxpr_as_fun(jaxprs.matvec), params.matvec, params_dot.matvec,
        jaxprs.matvec.jaxpr.debug_info, *x_leaves)
    rhs = _map(ad.add_tangents, b_dot, _map(operator.neg, matvec_tangents))

  x_dot = linear_solve_p.bind(*(_flatten(params) + rhs), **kwargs)

  # split into x tangents and aux tangents (these become zero)
  dx_leaves, daux_leaves = split_list(x_dot, [num_x_leaves])

  daux_leaves = _map(ad_util.p2tz, daux_leaves)

  x_dot = dx_leaves + daux_leaves

  return x, x_dot

