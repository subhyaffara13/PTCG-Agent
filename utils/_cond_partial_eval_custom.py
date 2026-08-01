
def _cond_partial_eval_custom(saveable, unks_in, inst_in, eqn):
  index_uk, *ops_uk = unks_in
  branches = eqn.params['branches']
  eqn_rest_params = dict(k_v for k_v in eqn.params.items() if k_v[0] != 'branches')

  # Instantiate all inputs (b/c jaxpr_staged will take all inputs).
  new_inst = [x for x, inst in zip(eqn.invars, inst_in)
              if type(x) is core.Var and not inst]
  del inst_in

  # NOTE(mattjj): I think it should be impossible for the index to be unknown,
  # but asserting that caused a test failure in diffrax. So we handle it: if it
  # is unknown, stage out the whole cond.
  if index_uk:
    all_true = [True] * len(branches[0].out_avals)
    return None, eqn, all_true, all_true, new_inst

  # First, compute output unknowns (unks_out), where an output of the cond is
  # unknown if it would be unknown on any of the branches.
  unks_out: list[bool] = [False] * len(eqn.outvars)
  for jaxpr in branches:
    _, _, unks_out_, _, _ = pe.partial_eval_jaxpr_custom(
        jaxpr.jaxpr, in_unknowns=ops_uk, in_inst=True,
        ensure_out_unknowns=False, ensure_out_inst=True, saveable=saveable)
    unks_out = map(operator.or_, unks_out, unks_out_)

  # Next, use the computed output unknowns to build a known jaxpr and a staged
  # jaxpr for each branch.
  branches_known_ : list[core.ClosedJaxpr] = []
  branches_staged_: list[core.ClosedJaxpr] = []
  branch_res_avals: list[list[core.AbstractValue]] = []
  for jaxpr in branches:
    jaxpr_known, jaxpr_staged, _, inst_out, num_res = \
        pe.partial_eval_jaxpr_custom(
            jaxpr.jaxpr, in_unknowns=ops_uk, in_inst=True,
            ensure_out_unknowns=unks_out, ensure_out_inst=True,
            saveable=saveable)
    branches_known_.append( core.ClosedJaxpr(jaxpr_known,  jaxpr.consts))
    branches_staged_.append(core.ClosedJaxpr(jaxpr_staged, jaxpr.consts))
    branch_res_avals.append(branches_staged_[-1].in_avals[:num_res])

  # Residuals may differ across branches, so we merge them, then use the merged
  # residuals to join the outputs of all branches to the same type.
  all_res_avals, res_avals_per_branch = _merge_branch_residuals(branch_res_avals)
  num_res = len(all_res_avals)
  num_known_outs = len(unks_out) - sum(unks_out)
  branches_known = _join_cond_outputs(
      branches_known_, all_res_avals, res_avals_per_branch, num_known_outs)
  branches_staged = _join_cond_pe_staged_jaxpr_inputs(
      branches_staged_, all_res_avals, res_avals_per_branch)
  assert all(all(map(core.typematch, j.out_avals, branches_known[0].out_avals))
             for j in branches_known[1:])

  # Create residual variables.
  res_binders = map(core.Var, all_res_avals)

  # Build the known eqn.
  ins_known, _ = partition_list(unks_in, eqn.invars)  # includes index invar
  out_binders_known, _ = partition_list(unks_out, eqn.outvars)
  params_known = dict(branches=branches_known, **eqn_rest_params)
  effects_known = _join_cond_effects(branches_known)
  eqn_known = pe.new_jaxpr_eqn(
      ins_known, [*out_binders_known, *res_binders], cond_p, params_known,
      effects_known, eqn.source_info, eqn.ctx)

  # Build the staged eqn.
  _, out_binders_staged = partition_list(inst_out, eqn.outvars)
  params_staged = dict(branches=branches_staged, **eqn_rest_params)
  effects_staged = _join_cond_effects(branches_staged)
  eqn_staged = pe.new_jaxpr_eqn(
      [eqn.invars[0], *res_binders, *eqn.invars[1:]], out_binders_staged,
      cond_p, params_staged, effects_staged, eqn.source_info, eqn.ctx)

  new_vars = [*new_inst, *res_binders]
  return eqn_known, eqn_staged, unks_out, inst_out, new_vars

