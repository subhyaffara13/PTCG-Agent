
def check_no_aliases(
    fn_name: str, /, *, check_can_update: tp.Iterable[str] = (), **kwargs
):
  Attrs = namedtuple('Attrs', kwargs.keys())  # type: ignore[misc]
  container = Attrs(**kwargs)
  is_leaf = lambda x: isinstance(x, variablelib.Variable)
  seen: dict[int, jax.tree_util.KeyPath] = {}
  for path, leaf in jax.tree.leaves_with_path(container, is_leaf=is_leaf):
    if not isinstance(leaf, variablelib.Variable):
      continue

    assert isinstance(path[0], jax.tree_util.GetAttrKey)
    kwarg_name = path[0].name

    if kwarg_name in check_can_update:
      if not leaf._can_update:
        path_str = jax.tree_util.keystr(path)
        raise ValueError(
            f'Cannot return captured Variable of type {type(leaf).__name__} '
            f'from nnx.{fn_name}.\n'
            f'Found at path: {path_str}'
        )

    var_id = id(leaf)
    if var_id in seen:
      path_str = jax.tree_util.keystr(path)
      seen_path_str = jax.tree_util.keystr(seen[var_id])
      raise ValueError(
        f'Duplicate {leaf}\nfound at paths:\n\n'
        f'  - {seen_path_str}\n'
        f'  - {path_str}\n\n'
        f'nnx.{fn_name} with graph_updates=False does not support '
        'Variable aliasing (duplicate inputs, duplicate outputs, or '
        'input Variables returned as outputs). '
        f'Consider the following options:\n\n'
        f'1. Remove the duplicate Variables.\n'
        f'2. Create new Variables via nnx.clone() and use those instead.\n'
        f'3. Enable graph mode and graph updates by passing graph=True and '
        f'graph_updates=True to {fn_name}\n\n'
        f'  nnx.{fn_name}(..., graph=True, graph_updates=True)\n\n'
        f'4. Use nnx.compat.{fn_name} (sets graph and graph_updates to True '
        f'automatically)\n\n'
        f'  nnx.compat.{fn_name}(...)'
      )
    seen[var_id] = path

