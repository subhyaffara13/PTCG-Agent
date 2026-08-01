
def group_collections(
  xs: VariableDict, col_filters: Sequence[CollectionFilter]
) -> Sequence[MutableVariableDict]:
  """Groups variables by collection filters.

  Iteratively applies the filters in `col_filters` to `xs`, and adds the result
  of applying each filter to the output sequence. Each key in `xs` is only added
  to the output once.

  Args:
    xs: a dictionary of variables, keyed by collections (strings).
    col_filters: a list of collection filters.

  Returns:
    A sequence S with `len(S) == len(col_filters)`. Each `S[i]` is the result of
    applying filter `col_filters[i]` to the remaining keys in `xs`.
  """
  cols: Iterable[str]
  cols = xs.keys()
  groups = []
  for col_filter in col_filters:
    remaining_cols = []
    group = {}
    for col in cols:
      if in_filter(col_filter, col):
        group[col] = jax.tree_util.tree_map(lambda x: x, xs[col])
      else:
        remaining_cols.append(col)
    cols = remaining_cols
    groups.append(group)
  return tuple(groups)

