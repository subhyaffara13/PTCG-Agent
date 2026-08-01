
def as_abstract(
    tree: A, graph: bool | None = None
) -> A:
  """Add sharding information to abstract Variables.

  When creating models with :func:`eval_shape`, Variables are abstract
  (backed by ``jax.ShapeDtypeStruct``) and may not carry sharding
  information, especially when using meshes with
  :attr:`jax.sharding.AxisType.Auto` axes. ``abstract_with_sharding`` inspects each
  Variable in ``tree`` and, if it has ``out_sharding`` metadata but no
  sharding already set, attaches a :class:`jax.sharding.NamedSharding`
  derived from the Variable's ``out_sharding`` and either its ``mesh``
  metadata or the current abstract mesh (``jax.sharding.get_abstract_mesh``).

  Example usage::

    from flax import nnx
    import jax

    mesh = jax.make_mesh((2, 2), ('a', 'b'),
      axis_types=(jax.sharding.AxisType.Auto,) * 2)
    with jax.set_mesh(mesh):
      abs_model = nnx.eval_shape(
        lambda: nnx.Linear(4, 8, rngs=nnx.Rngs(0),
          kernel_metadata={'out_sharding': ('a', 'b')}))
      abs_model = nnx.as_abstract(abs_model)
    assert abs_model.kernel.sharding.spec == jax.P('a', 'b')

  Args:
    tree: A graph node (e.g. an :class:`nnx.Module`) whose Variables should
      be annotated with sharding (via ``out_sharding`` metadata).
    graph: Forwarded to :func:`nnx.map`. If ``True``, uses graph-mode;
      if ``False``, uses tree-mode.
  Returns:
    A tree with sharding-annotated ShapeDtypeStruct values inside Variables.
  """
  def add_sharding(_path, x):
    if (
        isinstance(x, variablelib.Variable)
        and hasattr(value := x.get_value(), 'shape')
        and hasattr(value, 'dtype')
        and getattr(value, 'sharding', None) is None
        and x.has_metadata('out_sharding')
    ):
      if x.has_metadata('mesh'):
        mesh = x.get_metadata('mesh')
      else:
        mesh = jax.sharding.get_abstract_mesh()
      specs = get_var_pspec(x)
      sharding = jax.sharding.NamedSharding(mesh, specs)
      abs_var = x.replace(
          jax.ShapeDtypeStruct(value.shape, value.dtype, sharding=sharding)
      )
      return abs_var
    return x
  return graphlib.map(add_sharding, tree, graph=graph)

