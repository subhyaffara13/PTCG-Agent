
def prefix(
    node,
    filter_map: tp.Mapping[filterlib.Filter, tp.Any] | tp.Callable[..., tp.Any],
    /,
    *,
    graph: bool | None = None,
):
  """Replaces leaves in a graph node with prefix values.

  ``prefix`` replaces each leaf in ``node`` with a prefix value computed by
  ``filter_map(path, leaf)``. In graph mode (``graph=True``), the node is
  first converted to a tree and the prefix is applied to
  the resulting structure so it can be used directly as axes arguments for
  transforms like ``nnx.vmap``.

  Example usage::

    from flax import nnx
    import jax.numpy as jnp

    d = {'a': nnx.Param(jnp.array(2)), 'b': nnx.BatchStat(jnp.arange(5))}
    prefix = nnx.prefix(d, lambda path, x: 0 if 'b' in path else None)

    @nnx.vmap(in_axes=(prefix,))
    def f(d):
      return d['a'] * d['b']

    f(d)  # Array([0, 2, 4, 6, 8])

  ``filter_map`` can also be a mapping from :class:`Filter` to prefix values.
  Filters are checked in order and the first match determines the prefix::

    d = {'a': nnx.Param(jnp.array(2)), 'b': nnx.BatchStat(jnp.arange(5))}
    prefix = nnx.prefix(d, {nnx.Param: None, nnx.BatchStat: 0})

  Calculating prefixes for graph mode transforms is a bit more involved as
  the graph nodes are first converted to a trees in an order-dependent manner.
  This means prefixes should be calculated jointly between all graph nodes in
  the transform in the same order they appear in the arguments. For example::

    import jax
    import jax.numpy as jnp

    @nnx.vmap
    def create_model(rngs):
      return nnx.Linear(2, 3, rngs=rngs)

    model = create_model(nnx.Rngs(0).split(4))
    px1, px2 = nnx.prefix((model, model), {nnx.Param: 0}, graph=True)

    @nnx.vmap(in_axes=(px1, px2, None), graph=True)
    def forward(m1, m2, x):
      assert m1 is m2
      return m1(x) + m2(x)

    y = forward(model, model, jnp.ones(2))
    assert y.shape == (4, 3)

  The prefixes might be invalid if all graph node involved in the transform
  aren't passed to `nnx.prefix`.

  Args:
    node: A graph node object.
    filter_map: A callable ``(path, leaf) -> prefix`` that computes the prefix
      for each leaf, or a mapping from :class:`Filter` to prefix values (filters
      are checked in order; the first match determines the prefix).
    graph: If ``True``, uses graph-mode which supports the full NNX feature set
      including shared references. If ``False``, uses tree-mode which treats
      Modules as regular JAX pytrees, avoiding the overhead of the graph
      protocol.

  Returns:
    A new tree with prefix values replacing the leaves.
  """
  if graph is None:
    graph = graphlib.set_graph_mode.current_value()

  if isinstance(filter_map, tp.Mapping):
    predicates = tuple(
        (filterlib.to_predicate(f), value) for f, value in filter_map.items()
    )
    filters = list(filter_map.keys())

    def prefix_fn(path, leaf):
      for predicate, _prefix in predicates:
        if predicate(path, leaf):
          return _prefix
      raise ValueError(
          f'No filter matched leaf at path {path!r} with value {leaf!r}. '
          f'Filters: {filters}'
      )

  else:
    prefix_fn = filter_map

  is_leaf = lambda x: isinstance(x, variablelib.Variable)

  if graph:
    node = to_tree2(node, prefix_fn=prefix_fn)

  def _apply_prefix(jax_path, leaf):
    path = graphlib.jax_to_nnx_path(jax_path)
    if graph:
      # remove __state__ resulting from TreeState from path
      # to match the path you get on graph=False
      path = tuple(k for k in path if k != '__state__')
    return prefix_fn(path, leaf)

  return jax.tree.map_with_path(_apply_prefix, node, is_leaf=is_leaf)

