
def _map_submodules(fn: Callable[['Module'], Any], tree):
  """Map a function over all submodules in a tree."""
  g = lambda _, x: fn(x) if isinstance(x, Module) else x
  return _freeze_attr(_map_over_modules_in_tree(g, tree))

