
def _wgmma_ref_pp_eqn(
    eqn: jax_core.JaxprEqn,
    context: jax_core.JaxprPpContext,
    settings: jax_core.JaxprPpSettings,
):
  del settings
  acc, a, b, *leaves = eqn.invars
  transform_treedefs = [
      eqn.params["acc_transforms_tree"],
      eqn.params["a_transforms_tree"],
      eqn.params["b_transforms_tree"],
  ]
  transform_leaves = util.split_list(
      leaves, [getattr(tree, "num_leaves", 0) for tree in transform_treedefs]
  )
  acc_transforms, a_transforms, b_transforms = (
      () if treedef is None else treedef.unflatten(leaves)
      for treedef, leaves in zip(transform_treedefs, transform_leaves)
  )
  return pp.concat([
      pp.text("wgmma_ref"),
      pp.text(" "),
      state_primitives.pp_ref_transforms(context, acc, acc_transforms),
      pp.text(" <- "),
      state_primitives.pp_ref_transforms(context, a, a_transforms),
      pp.text(" @ "),
      state_primitives.pp_ref_transforms(context, b, b_transforms),
  ])

