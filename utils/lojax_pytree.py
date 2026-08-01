
def lojax_pytree(hi_avals, tree):
  lo_avals = [t.lo_ty() for t in hi_avals]
  return tree_util.tracing_registry.flatten(tree_unflatten(tree, lo_avals))[1]

