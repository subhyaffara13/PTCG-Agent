
def _scan_remat(policy, *args, jaxpr, **params):
  jaxpr_fwd, jaxpr_rem_, num_res = remat.remat_jaxpr(jaxpr, policy)
  all_out = scan_p.bind(*args, jaxpr=jaxpr_fwd, **params)
  primals_out, res = split_list(all_out, [len(jaxpr.outvars)])
  jaxpr_rem = pe.move_binders_to_back(jaxpr_rem_, [True] * num_res)
  def rem(*args):
    return scan_p.bind(*args, *res, jaxpr=jaxpr_rem, **params)
  return primals_out, rem

