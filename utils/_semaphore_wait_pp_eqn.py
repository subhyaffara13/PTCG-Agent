
def _semaphore_wait_pp_eqn(eqn: jax_core.JaxprEqn,
                             context: jax_core.JaxprPpContext,
                             settings: jax_core.JaxprPpSettings):
  del settings
  invars = eqn.invars
  tree = eqn.params["args_tree"]
  (
      sem,
      sem_transforms,
      value,
      decrement,
  ) = tree_util.tree_unflatten(tree, invars)
  parts = [
      pp.text("semaphore_wait"),
  ]
  if decrement:
    parts.append(pp.text("[dec]"))
  parts += [
      pp.text(" "),
      sp.pp_ref_transforms(context, sem, sem_transforms),
      pp.text(" "),
      jax_core.pp_var(value, context),
  ]
  return pp.concat(parts)

