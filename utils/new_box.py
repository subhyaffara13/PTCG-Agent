
def new_box():
  (), treedef = tree_flatten(None)
  return new_box_p.bind(treedef=treedef)

