
def _construct_fusion_jaxpr(
    candidate_values, jaxpr: jax_core.Jaxpr, outvars, *invars, **kwargs
):
  flat_outvars, out_tree = tree_util.tree_flatten(outvars)
  flat_invars, in_tree = tree_util.tree_flatten((invars, kwargs))
  new_jaxpr_no_dce = jaxpr.replace(
      outvars=flat_outvars,
      constvars=jaxpr.constvars + jaxpr.invars,
      invars=flat_invars,
      debug_info=jaxpr.debug_info.with_unknown_names()
  )
  new_jaxpr, used_consts, used_invars = pe.dce_jaxpr_consts(
      new_jaxpr_no_dce,
      [True] * len(new_jaxpr_no_dce.outvars),
      instantiate=[False] * len(new_jaxpr_no_dce.constvars)
      + [True] * len(new_jaxpr_no_dce.invars),
  )
  assert all(used_invars), new_jaxpr_no_dce
  new_values = tuple(
      c for used, c in zip(used_consts, candidate_values, strict=True) if used
  )
  kernel_in_tree = tree_util.tree_structure((invars, kwargs))
  flat_in_type = [x.aval for x in flat_invars]
  in_type = tree_util.tree_unflatten(kernel_in_tree, flat_in_type)
  out_type = tree_util.tree_unflatten(
      out_tree,
      [x.aval for x in flat_outvars],
  )
  return new_jaxpr, new_values, in_type, out_type, out_tree

