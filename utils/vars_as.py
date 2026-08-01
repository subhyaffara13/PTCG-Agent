
def vars_as(
  node: A,
  /,
  *,
  hijax: bool | None = None,
  ref: bool | None = None,
  mutable: bool | None = None,
  only: filterlib.Filter = ...,
  allow_duplicates: bool = False,
) -> A:
  """ """
  new_attrs: dict[str, bool] = {}
  if hijax is not None:
    new_attrs['hijax'] = hijax
  if ref is not None:
    new_attrs['ref'] = ref
  if mutable is not None:
    new_attrs['mutable'] = mutable

  def _different_vars(path, x):
    return isinstance(x, Variable) and any(
      getattr(x, attr) != value for attr, value in new_attrs.items()
    )

  only = filterlib.All(_different_vars, only)
  predicate = filterlib.to_predicate(only)

  if not allow_duplicates and (
    all_duplicates := find_duplicates(node, only=only)
  ):
    duplicates_strs = '\n  ---'
    for node_duplicates in all_duplicates:
      for path in node_duplicates:
        path_str = '/'.join(builtins.map(str, path))
        duplicates_strs += f'\n  {path_str}'
      duplicates_strs += '\n  ---'
    raise ValueError(f'Found duplicate at paths:{duplicates_strs}')

  def _to_refs(jax_path, x):
    if predicate(jax_to_nnx_path(jax_path), x):
      assert isinstance(x, Variable)
      variable = x.copy(**new_attrs)
      return variable
    return x

  node = jax.tree.map_with_path(
    _to_refs, node, is_leaf=lambda x: isinstance(x, Variable)
  )
  return node

