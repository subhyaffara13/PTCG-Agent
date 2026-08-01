
def _dedup_scopes(scopes):
  """Deduplicated scopes."""
  paths = []
  # must preseve insertion order for duplication to work correctly
  minimal_set = collections.OrderedDict((s, ()) for s in scopes)
  for leaf in scopes:
    scope = leaf.parent
    max_parent = leaf
    max_parent_path = ()
    path = [leaf.name]
    while scope is not None:
      if scope in minimal_set:
        max_parent = scope
        max_parent_path = tuple(reversed(path))
      path.append(scope.name)
      scope = scope.parent
    if max_parent is not leaf and leaf in minimal_set:
      del minimal_set[leaf]
    paths.append((max_parent, max_parent_path))
  return tuple(minimal_set), tuple(paths)

