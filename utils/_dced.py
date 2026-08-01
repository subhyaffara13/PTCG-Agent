
def _dced(jaxpr, out_tree, res, *args):
  out_flat = core.eval_jaxpr(jaxpr.jaxpr, jaxpr.consts, *res, *args)
  return tree_unflatten(out_tree, out_flat)

