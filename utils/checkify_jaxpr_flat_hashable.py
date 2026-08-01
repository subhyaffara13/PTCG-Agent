
def checkify_jaxpr_flat_hashable(jaxpr, hashable_consts, enabled_errors,
                                 err_tree, *args):
  consts = tuple(c.x for c in hashable_consts)
  return checkify_jaxpr_flat(jaxpr, consts, enabled_errors, err_tree, *args)

