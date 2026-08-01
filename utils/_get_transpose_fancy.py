
def _get_transpose_fancy(g, ref_, *idx, tree):
  transforms = tree_util.tree_unflatten(tree, idx)
  if transforms and type(g) is not ad_util.Zero:
    addupdate_p.bind(ref_.inst().ref, g, *idx, tree=tree)
  else:
    ref_.accum(g)

