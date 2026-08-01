
def make_args_info(in_tree, in_avals, donate_argnums):
  donate_argnums = frozenset(donate_argnums)
  flat_avals, _ = tree_util.tree_flatten(in_avals)  # todo: remove
  return in_tree.unflatten([
      ArgInfo(aval, i in donate_argnums)
      for i, aval in enumerate(flat_avals)])

