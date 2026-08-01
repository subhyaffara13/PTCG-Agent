
def _pjit_remat(policy, *args, jaxpr, **params):
  jaxpr_fwd, jaxpr_rem, num_res = remat.remat_jaxpr(jaxpr, policy)
  params_fwd, params_rem = _add_res_to_params(num_res, **params)
  primals_res_out = jit_p.bind(*args, jaxpr=jaxpr_fwd, **params_fwd)
  primals_out, res = split_list(primals_res_out, [len(jaxpr.outvars)])
  return primals_out, partial(jit_p.bind, *res, jaxpr=jaxpr_rem, **params_rem)

