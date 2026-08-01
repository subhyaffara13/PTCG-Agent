
def _get_new_mesh(axes: str | tuple[str, ...] | None,
                  axis_type: mesh_lib.AxisType, name: str, shardings=None
                  ) -> MeshInfo | None:
  cur_mesh = mesh_lib.get_abstract_mesh()
  flat_shardings, _ = tree_flatten(shardings)
  sharding_mesh = mesh_lib.empty_abstract_mesh
  for i in flat_shardings:
    if isinstance(i, NamedSharding):
      if not sharding_mesh.empty and sharding_mesh != i.mesh.abstract_mesh:
        raise ValueError(
            f'Shardings passed to {name} should have the same mesh. Got one'
            f' mesh {sharding_mesh} and another {i.mesh}')
      sharding_mesh = i.mesh.abstract_mesh

  if sharding_mesh.empty and cur_mesh.empty:
    return None
  if not sharding_mesh.empty and not cur_mesh.empty:
    if sharding_mesh != cur_mesh:
      raise ValueError(
          f'Context mesh {cur_mesh} must match the mesh passed to shardings'
          f' {sharding_mesh}. Recommended approach is to use'
          ' `jax.set_mesh` context manager.')
    mesh_to_use = cur_mesh
  elif sharding_mesh.empty and not cur_mesh.empty:
    mesh_to_use = cur_mesh
  else:
    assert not sharding_mesh.empty and cur_mesh.empty
    mesh_to_use = sharding_mesh

  if axes is None:
    axes = mesh_to_use.axis_names
  if not isinstance(axes, tuple):
    axes = (axes,)
  for a in axes:
    if (mesh_to_use._name_to_type[a] == mesh_lib.AxisType.Manual and
        axis_type in {mesh_lib.AxisType.Auto, mesh_lib.AxisType.Explicit}):
      raise NotImplementedError(
          'Going from `Manual` AxisType to `Auto` or `Explicit` AxisType is not'
          ' allowed. Please file a bug at https://github.com/jax-ml/jax/issues'
          ' with your use case')
  new_mesh = mesh_to_use.update_axis_types({a: axis_type for a in axes})
  return MeshInfo(prev=mesh_to_use, new=new_mesh, axes=axes)

