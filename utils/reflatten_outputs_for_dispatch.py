
def reflatten_outputs_for_dispatch(out_tree, out_flat):
  # We arrive at dispatch having flattened according to the default
  # pytree registry, but we want to re-flatten according to our
  # dispatch-specific registry.
  out_unflat = tree_util.tree_unflatten(out_tree, out_flat)
  return tree_util.dispatch_registry.flatten(out_unflat, None)

