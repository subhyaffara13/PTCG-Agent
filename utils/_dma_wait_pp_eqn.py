
def _dma_wait_pp_eqn(eqn: jax_core.JaxprEqn,
                     context: jax_core.JaxprPpContext,
                     settings: jax_core.JaxprPpSettings):
  del settings
  invars = eqn.invars
  tree = eqn.params["tree"]
  _, ref, sem, _, _ = _dma_unflatten(tree, invars)
  return pp.concat([
      pp.text("dma_wait"),
      pp.text(" "),
      sp.pp_ref_transforms(context, ref),
      pp.text(" "),
      sp.pp_ref_transforms(context, sem),
  ])

