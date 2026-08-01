
def _cond_remat(policy, *args, branches, **params):
  branches_fwd, branches_rem, branch_res_avals = [], [], []
  for jaxpr in branches:
    jaxpr_fwd, jaxpr_rem, num_res = remat.remat_jaxpr(jaxpr, policy)
    branches_fwd.append(jaxpr_fwd)
    branches_rem.append(jaxpr_rem)
    _, res_avals = split_list_checked(jaxpr_fwd.out_avals, [len(jaxpr.out_avals), num_res])
    branch_res_avals.append(res_avals)
  merged_avals, branch_res_avals = _merge_branch_residuals(branch_res_avals)
  branches_fwd = _join_cond_outputs(
      branches_fwd, merged_avals, branch_res_avals, len(jaxpr.out_avals))
  branches_rem = _join_cond_pe_staged_jaxpr_inputs(
      branches_rem, merged_avals, branch_res_avals)
  all_out = cond_p.bind(*args, branches=branches_fwd, **params)
  primals_out, res = split_list(all_out, [len(jaxpr.out_avals)])
  def rem(idx, *args):
    return cond_p.bind(idx, *res, *args, branches=branches_rem, **params)
  return primals_out, rem

