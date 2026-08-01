
def all_dim_vars(args_avals: Sequence[core.ShapedArray]) -> Sequence[str]:
  dim_vars: set[str] = set()
  for a in args_avals:
    for d in a.shape:
      if is_symbolic_dim(d):
        dim_vars = dim_vars.union(d._get_vars())
  return sorted(dim_vars)

