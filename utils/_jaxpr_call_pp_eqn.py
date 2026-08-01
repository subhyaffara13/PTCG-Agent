
def _jaxpr_call_pp_eqn(
    eqn: jax_core.JaxprEqn,
    context: jax_core.JaxprPpContext,
    settings: jax_core.JaxprPpSettings,
):
  flat_args = eqn.invars
  ref_treedefs = eqn.params["ref_treedefs"]
  flat_refs, _ = util.split_list(
      flat_args, [sum(treedef.num_leaves for treedef in ref_treedefs)]
  )
  flat_refs = util.split_list(
      flat_refs,
      [treedef.num_leaves for treedef in ref_treedefs[: len(ref_treedefs) - 1]],
  )
  trailer = []
  for treedef, flat_ref in zip(ref_treedefs, flat_refs):
    ref = treedef.unflatten(flat_ref)
    transforms = []
    if isinstance(ref, tuple):
      ref, transforms = ref
    trailer.append(pp.text(" "))
    trailer.append(sp.pp_ref_transforms(context, ref, transforms))
  return pp.concat([
      pp.text("jaxpr_call"),
      pp.text("["),
      jax_core.pp_kv_pair("jaxpr", eqn.params["jaxpr"], context, settings),
      pp.text("]"),
      pp.concat(trailer),
  ])

