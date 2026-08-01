
def filter_statics_from_treedef(registry, treedef, statics):
  if statics is False:
    return treedef
  elif statics is True:
    assert False, "unreachable"
  elif isinstance(statics, tuple):
    filtered = tuple(
        filter_statics_from_treedef(registry, td, s)
        for td, s in zip(treedef.children(), statics) if s is not True)
    return treedef.from_node_data_and_children(registry, treedef.node_data(), filtered)
  elif isinstance(statics, dict):
    ty, keys = treedef.node_data()
    filtered_keys, filtered_subtrees = unzip2(
        (k, filter_statics_from_treedef(registry, td, statics[k]))
        for td, k in zip(treedef.children(), keys) if statics[k] is not True)
    return treedef.from_node_data_and_children(registry, (ty, filtered_keys), filtered_subtrees)
  else:
    assert False, "unreachable"

