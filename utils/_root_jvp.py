
def _root_jvp(const_lengths, jaxprs, primals, tangents):
  params, _ = _split_root_args(primals, const_lengths)
  sol = _custom_root(const_lengths, jaxprs, *primals)

  f_out_vals = len(jaxprs.f.out_avals)
  solution, aux = split_list(sol, [f_out_vals])

  params_dot, _ = _split_root_args(tangents, const_lengths)

  # F(m, u) = 0      # system of equations in u, parameterized by m
  #                  # solution is u*(m) defined in a neighborhood
  # F(m, u*(m)) = 0  # satisfied in a neighborhood
  #
  # ∂_0 F(m, u*(m)) + ∂_1 F(m, u*(m)) ∂ u*(m) = 0       # implied by line above
  # ∂ u*(m) = - (∂_1 F(m, u*(m)))^{-1} ∂_0 F(m, u*(m))  # rearrange
  #
  # ∂ u*(m)[v] = - (∂_1 F(m, u*(m)))^{-1} [∂_0 F(m, u*(m))[v]]  # jvp

  f = core.jaxpr_as_fun(jaxprs.f)
  linearize_and_solve = partial(
      core.jaxpr_as_fun(jaxprs.l_and_s), *params.l_and_s)
  f_at_solution = lambda *params: f(*params, *solution)
  _, rhs = ad.jvp(f_at_solution, FlatTree.flatten_list(params.f),
                  FlatTree.flatten_list(params_dot.f))
  solution_dot = _map(
      operator.neg, linearize_and_solve(*solution, *rhs))
  # append aux, create symbolic zero tangents for the aux values
  solution += aux
  solution_dot += _map(ad_util.zeros_like_jaxval, aux)

  return solution, solution_dot

