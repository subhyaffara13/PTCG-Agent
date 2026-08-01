
def _cond_partial_eval(trace, *tracers, branches, **params):
  in_unknowns = [not t.pval.is_known() for t in tracers]
  index_uk, *ops_uk = in_unknowns
  if any(isinstance(eff, RefEffect) for branch in branches for eff in
      branch.jaxpr.effects):
    raise NotImplementedError(
        "State effect not supported in cond partial-eval.")

  if index_uk:
    # When the branch index is unknown, we stage out the whole cond.
    # TODO(mattjj): remove this path when old remat is removed
    params = dict(branches=branches, **params)
    return trace.default_process_primitive(cond_p, tracers, params)

  branches_out_uks = []
  for branch_jaxpr in branches:
    _, _, out_uks, _ = pe.partial_eval_jaxpr_nounits(
        branch_jaxpr, ops_uk, instantiate=False)
    branches_out_uks.append(out_uks)
  out_uks = [any(uks) for uks in zip(*branches_out_uks)]

  branches_known, branches_unknown, branch_res_avals = [], [], []
  for branch_jaxpr in branches:
    branch_jaxpr_known, branch_jaxpr_unknown, _, res_avals = \
        pe.partial_eval_jaxpr_nounits(branch_jaxpr, ops_uk, instantiate=out_uks)
    branches_known.append(branch_jaxpr_known)
    branches_unknown.append(branch_jaxpr_unknown)
    branch_res_avals.append(res_avals)

  all_res_avals, res_avals_per_branch = _merge_branch_residuals(branch_res_avals)
  num_res = len(all_res_avals)

  num_known_outs = len(out_uks) - sum(out_uks)
  branches_known = _join_cond_outputs(
      branches_known, all_res_avals, res_avals_per_branch, num_known_outs)
  branches_unknown = _join_cond_pe_staged_jaxpr_inputs(
      branches_unknown, all_res_avals, res_avals_per_branch)
  assert all(all(map(core.typematch, j.out_avals, branches_known[0].out_avals))
             for j in branches_known[1:])

  in_consts = [t.pval.get_known() for t in tracers if t.pval.is_known()]
  out_consts_res = cond_p.bind(*in_consts, branches=branches_known,
                               **params)
  out_consts, res = split_list(out_consts_res, [len(out_consts_res) - num_res])

  index_tracer = trace.instantiate_const(tracers[0])
  ops_tracers = [trace.instantiate_const(t)
                 for uk, t in zip(in_unknowns[1:], tracers[1:]) if uk]
  res_tracers = map(trace.new_instantiated_const, res)
  out_tracers = [pe.JaxprTracer(trace, pe.PartialVal.unknown(aval), None)
                 for aval in branches_unknown[0].out_avals]
  params = dict(branches=branches_unknown, **params)
  name_stack = source_info_util.current_name_stack()[len(trace.name_stack):]
  source = source_info_util.current().replace(name_stack=name_stack)
  eqn = pe.new_eqn_recipe(
      trace, [index_tracer] + res_tracers + ops_tracers, out_tracers, cond_p, params,
      _join_cond_effects(branches_unknown), source)
  for t in out_tracers: t.recipe = eqn
  return util.merge_lists(out_uks, out_consts, out_tracers)

