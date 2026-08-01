
def check_prefix(
  prefix: tp.Any,
  prefix_name: str,
  fn_name: str,
  graph: bool,
  graph_updates: bool,
):
  def _check(path, leaf):
    if isinstance(leaf, variablelib.Variable):
      raise ValueError(
        f'Found Variable of type {type(leaf).__name__} '
        f'at path {jax.tree_util.keystr(path)} in `{prefix_name}` '
        f'for nnx.{fn_name}. Variables prefixes are not supported.'
        f'Pass a prefix for the entire Variable instead of passing a '
        f'Variable with a prefix for its value.'
      )
    if isinstance(leaf, PrefixMapping) and not (graph and graph_updates):
      raise ValueError(
        f'`{prefix_name}` cannot contain `{type(leaf).__name__}` objects '
        f'when `graph=False` or `graph_updates=False`. '
        f'Consider the following options:\n\n'
        f'1. Remove `{type(leaf).__name__}` objects from `{prefix_name}`.\n'
        f'2. Enable graph mode and graph updates by passing graph=True and '
        f'graph_updates=True to {fn_name} e.g.\n\n'
        f'  nnx.{fn_name}(..., graph=True, graph_updates=True)\n\n'
        f'3. Use nnx.compat.{fn_name} instead e.g.\n\n'
        f'  nnx.compat.{fn_name}(...)'
      )
    if graphlib.is_graph_node(leaf) and graph:
      raise ValueError(
        f'Found graph node of type {type(leaf).__name__} '
        f'at path {jax.tree_util.keystr(path)} in `{prefix_name}` '
        f'for nnx.{fn_name}. Graph nodes are not allowed as prefixes when '
        f'graph=True.'
        f'Consider the following options:\n\n'
        f'1. Remove graph nodes from `{prefix_name}`.\n'
        f'2. Enable tree mode by passing graph=False to {fn_name} e.g.\n\n'
        f'  nnx.{fn_name}(..., graph=False)\n\n'
        f'3. If you using nnx.prefix to create the prefix, pass graph=True:\n\n'
        f'  prefix = nnx.prefix(..., graph=True)'
      )
    if isinstance(leaf, TreeState) and (not graph or graph_updates):
      msg = (
        f'Found `TreeState` object at path {jax.tree_util.keystr(path)} in '
        f'`{prefix_name}` for nnx.{fn_name}. `TreeState` objects are only '
        f'allowed as prefixes when `graph=True` and `graph_updates=False`.'
        f'Consider the following options:\n\n'
        f'1. Enable graph mode and graph updates by passing graph=True and '
        f'graph_updates=True to {fn_name} e.g.\n\n'
        f'  nnx.{fn_name}(..., graph=True, graph_updates=True)\n\n'
        f'2. Use nnx.compat.{fn_name} instead e.g.\n\n'
        f'  nnx.compat.{fn_name}(...)'
      )
      if graph_updates:
        msg += (
          f'\n\n3. If you using nnx.prefix to create the prefix, pass graph=False:\n\n'
          f'  prefix = nnx.prefix(..., graph=False)'
        )
      raise ValueError(msg)

  jax.tree.map_with_path(
    _check,
    prefix,
    is_leaf=lambda x: isinstance(x, variablelib.Variable)
    or graphlib.is_graph_node(x)
    or isinstance(x, PrefixMapping)
    or isinstance(x, TreeState),
  )

