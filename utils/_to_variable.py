
def _to_variable(node):
  # import here to avoid circular imports
  from flax.nnx.spmd import get_var_pspec

  def to_variable(x):
    if isinstance(x, ValueMetadata):
      var = x.var_type._new(x.value, x.metadata)

      global_mesh = jax.sharding.get_abstract_mesh()
      if global_mesh.axis_sizes == ():
        global_mesh = None
      mesh = var.get_metadata("mesh", None) or global_mesh
      if mesh is not None and (not hasattr(var, 'sharding') or var.sharding is None):
        pspec = get_var_pspec(var)
        sharding = jax.sharding.NamedSharding(mesh=mesh, spec=pspec)
        var.set_value(jax.ShapeDtypeStruct(shape=var.shape, dtype=var.dtype, sharding=sharding))
      return var
    return x

  return jax.tree.map(
    to_variable, node, is_leaf=lambda x: isinstance(x, ValueMetadata)
  )

