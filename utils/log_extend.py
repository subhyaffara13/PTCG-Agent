
def log_extend(log, dct):
  leaves, treedef = tree_flatten(dct)
  log_extend_p.bind(log, *leaves, treedef=treedef)

