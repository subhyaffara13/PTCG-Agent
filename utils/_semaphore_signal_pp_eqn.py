
def _semaphore_signal_pp_eqn(eqn: jax_core.JaxprEqn,
                             context: jax_core.JaxprPpContext,
                             settings: jax_core.JaxprPpSettings):
  del settings
  invars = eqn.invars
  tree = eqn.params["args_tree"]
  (
      sem,
      sem_transforms,
      value,
      device_ids,
      _,
  ) = tree_util.tree_unflatten(tree, invars)
  out = pp.concat([
      pp.text("semaphore_signal"),
      pp.text(" "),
      sp.pp_ref_transforms(context, sem, sem_transforms),
      pp.text(" "),
      jax_core.pp_var(value, context),
  ])
  if device_ids is not None:
    flat_device_ids = tree_util.tree_leaves(device_ids)
    if not flat_device_ids:
      return out
    out = pp.concat([out, pp.text(" "), _pp_device_id(device_ids, context)])
  return out

