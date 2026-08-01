
def _join_cond_pe_staged_jaxpr_inputs(
    jaxprs: Sequence[core.ClosedJaxpr], all_res_avals,
    res_aval_indices_per_jaxpr) -> tuple[core.ClosedJaxpr, ...]:
  all_res_vars = map(core.Var, all_res_avals)

  def augment_jaxpr(jaxpr: core.ClosedJaxpr, res_indices) -> core.ClosedJaxpr:
    num_res = len(res_indices)
    res_vars = jaxpr.jaxpr.invars[:num_res]
    non_res_vars = jaxpr.jaxpr.invars[num_res:]

    aug_res_vars = list(util.subvals(all_res_vars, zip(res_indices, res_vars)))
    aug_invars = aug_res_vars + non_res_vars
    jaxpr_aug = jaxpr.jaxpr.replace(invars=aug_invars)
    return core.ClosedJaxpr(jaxpr_aug, jaxpr.consts)

  return tuple(map(augment_jaxpr, jaxprs, res_aval_indices_per_jaxpr))

