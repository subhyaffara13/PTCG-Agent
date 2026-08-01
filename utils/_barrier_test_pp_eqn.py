
def _barrier_test_pp_eqn(
    eqn: jax_core.JaxprEqn,
    context: jax_core.JaxprPpContext,
    settings: jax_core.JaxprPpSettings,
):
  del settings
  barrier, *flat_transforms = eqn.invars
  transforms_treedef = eqn.params["transforms_treedef"]
  transforms = transforms_treedef.unflatten(flat_transforms)
  return pp.concat([
      pp.text("barrier_test"),
      pp.text(" "),
      state_primitives.pp_ref_transforms(context, barrier, transforms),
  ])

