
def flat_out_axes(
    f: lu.WrappedFun, out_spec: Any
) -> tuple[lu.WrappedFun, Callable]:
  leaves, treedef = tree_flatten(out_spec)
  f, out_axes = _flat_out_axes(f, tuple(leaves), treedef)
  return f, HashableFunction(out_axes, closure=(tuple(leaves), treedef))

