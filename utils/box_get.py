
def box_get(box):
  tys = core.cur_qdd(box)
  leaf_vals = box_get_p.bind(box, avals=tuple(tys.leaf_avals))
  return tree_unflatten(tys.treedef, leaf_vals)

