from typing import Optional

def setup_sharded_pytree(
    pytree: Optional[pytree_checkpoint_handler.PyTree] = None,
    reverse_devices: bool = False,
    devices: Optional[list[jax.Device]] = None,
):
  """Creates a PyTree of sharded arrays for testing."""
  if devices is None:
    devices = jax.devices()
  num_devices = len(devices)
  if reverse_devices:
    devices = np.asarray(list(reversed(devices)))
  else:
    devices = np.asarray(devices)

  mesh_2d = jax.sharding.Mesh(
      devices.reshape((2, num_devices // 2)), ('x', 'y')
  )
  mesh_axes_2d = jax.sharding.PartitionSpec('x', 'y')
  mesh_1d = jax.sharding.Mesh(devices, ('x',))
  mesh_axes_1d = jax.sharding.PartitionSpec(
      'x',
  )
  mesh_0d = jax.sharding.Mesh(devices, ('x',))
  mesh_axes_0d = jax.sharding.PartitionSpec(
      None,
  )

  if pytree is None:
    pytree = setup_pytree()
  mesh_tree = {
      'a': mesh_0d,
      'b': mesh_1d,
      'c': {
          'a': mesh_2d,
          'e': mesh_2d,
      },
  }
  axes_tree = {
      'a': mesh_axes_0d,
      'b': mesh_axes_1d,
      'c': {
          'a': mesh_axes_2d,
          'e': mesh_axes_2d,
      },
  }

  pytree = jax.tree.map(
      create_sharded_array, pytree, mesh_tree, axes_tree, is_leaf=is_leaf
  )
  return pytree, mesh_tree, axes_tree

