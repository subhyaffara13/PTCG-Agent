
def _dma_start_pp_eqn(eqn: jax_core.JaxprEqn,
                      context: jax_core.JaxprPpContext,
                      settings: jax_core.JaxprPpSettings):
  invars = eqn.invars
  tree = eqn.params["tree"]
  priority = eqn.params["priority"]
  add = eqn.params["add"]
  src_ref, dst_ref, dst_sem, src_sem, device_id = _dma_unflatten(tree, invars)
  # TODO(sharadmv): pretty print source semaphores and device id
  if src_sem or device_id:
    return jax_core._pp_eqn(eqn, context, settings)
  return pp.concat([
      pp.text(f"dma_start(p{priority}{', add' if add else ''})"),
      pp.text(" "),
      sp.pp_ref_transforms(context, src_ref),
      pp.text(" -> "),
      sp.pp_ref_transforms(context, dst_ref),
      pp.text(" "),
      sp.pp_ref_transforms(context, dst_sem),
  ])

