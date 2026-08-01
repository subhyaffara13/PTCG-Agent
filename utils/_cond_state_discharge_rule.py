
def _cond_state_discharge_rule(should_discharge, in_avals, out_avals, index, *args,
                               branches, **params):
  assert not should_discharge[0], "Can't discharge the index."
  discharged_branches = tuple(
      discharge_state(branch, should_discharge=should_discharge[1:])
      for branch in branches
  )
  # Don't thread the ref values through the cond if they never change.
  forwarded_outvars: list[int | None] | None = None
  for branch in discharged_branches:
    invar_pos = {v: i for i, v in enumerate(branch.invars)}
    branch_forwarding = [
        invar_pos.get(v, None) if isinstance(v, core.Var) else None
        for v in branch.outvars[len(out_avals) :]]
    if forwarded_outvars is None:
      forwarded_outvars = branch_forwarding
    else:
      forwarded_outvars = [
          i if i == j else None
          for i, j in zip(forwarded_outvars, branch_forwarding)]
  assert forwarded_outvars is not None
  all_outvars_fwd = [None] * len(out_avals) + forwarded_outvars
  new_branches = tuple(
      branch.replace(
          jaxpr=branch.jaxpr.replace(
              outvars=[v for v, fwd in zip(branch.outvars, all_outvars_fwd) if fwd is None]
          )
      )
      for branch in discharged_branches
  )
  out_vals_no_fwd = cond_p.bind(index, *args, branches=new_branches,
                                **params)
  out_vals, out_ref_vals_no_fwd = util.split_list(out_vals_no_fwd, [len(out_avals)])
  # Insert forwarded values into reference outputs
  ref_val_no_fwd_iter = iter(out_ref_vals_no_fwd)
  out_ref_vals = [next(ref_val_no_fwd_iter) if fwd is None else args[fwd]
                  for fwd in forwarded_outvars]
  # Map reference outputs back to their invars
  ref_val_iter = iter(out_ref_vals)
  new_invals = []
  for should, aval in zip(should_discharge, in_avals):
    discharged_inval = isinstance(aval, AbstractRef) and should
    new_invals.append(next(ref_val_iter) if discharged_inval else None)
  return new_invals, out_vals

