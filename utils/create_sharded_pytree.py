
def create_sharded_pytree(
    *,
    add: int = 0,
    reverse_devices: bool = False,
    include_scalars: bool = True,
    replicated_arrays: bool = False,
    devices: list[jax.Device] | None = None,
    slices: int = 2,
) -> tuple[tree_types.PyTree, tree_types.PyTree]:
  """Creates a sharded PyTree from `create_numpy_pytree`.

  Args:
    add: The value to add to leaf arrays.
    reverse_devices: Whether to reverse the devices in the mesh.
    include_scalars: Whether to include scalars in the pytree.
    replicated_arrays: Whether to replicate arrays across devices.
    devices: The devices to use for the mesh.
    slices: The number of slices to use for the mesh.

  Returns:
    A tuple of (pytree, abstract_pytree).
  """
  if devices is None:
    devices = jax.devices()
  num_devices = len(devices)
  devices = (
      np.asarray(list(reversed(devices)))
      if reverse_devices
      else np.asarray(devices)
  )

  mesh_2d = jax.sharding.Mesh(
      devices.reshape((slices, num_devices // slices)), ('x', 'y')
  )
  mesh_axes_2d = jax.sharding.PartitionSpec('x', 'y')
  if replicated_arrays:
    mesh_axes_2d = jax.sharding.PartitionSpec(None, 'y')
  mesh_1d = jax.sharding.Mesh(devices, ('x',))
  mesh_axes_1d = jax.sharding.PartitionSpec(
      'x',
  )
  if replicated_arrays:
    mesh_axes_1d = jax.sharding.PartitionSpec(None,)
  mesh_0d = jax.sharding.Mesh(devices, ('x',))
  mesh_axes_0d = jax.sharding.PartitionSpec(
      None,
  )

  shardings = {
      'a': jax.sharding.NamedSharding(mesh_0d, mesh_axes_0d),
      'b': jax.sharding.NamedSharding(mesh_1d, mesh_axes_1d),
      'c': {
          'a': jax.sharding.NamedSharding(mesh_2d, mesh_axes_2d),
          'e': jax.sharding.NamedSharding(mesh_2d, mesh_axes_2d),
      },
  }
  if include_scalars:
    scalar_axes = jax.sharding.PartitionSpec()
    shardings.update({
        'x': jax.sharding.NamedSharding(mesh_0d, scalar_axes),
        'y': jax.sharding.NamedSharding(mesh_0d, scalar_axes),
    })
  pytree, _ = create_numpy_pytree(add=add, include_scalars=include_scalars)
  pytree = jax.tree.map(create_sharded_array, pytree, shardings)
  return pytree, jax.tree.map(as_abstract_type, pytree)

