
def box_set(box, val):
  leaves, treedef = tree_flatten(val)
  box_set_p.bind(box, *leaves, treedef=treedef)

