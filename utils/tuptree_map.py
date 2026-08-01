
def tuptree_map(f, treedef, x):
  return treedef.walk(lambda xs, _: tuple(xs), f, x)

