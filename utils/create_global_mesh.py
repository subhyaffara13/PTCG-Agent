import logging

def create_global_mesh(
    num_slices: int,
    *,
    replica_axis_index: int = 0,
    data_parallelism: int | None = None,
    tensor_parallelism: int | None = None,
    fsdp_parallelism: int | None = None,
) -> jax.sharding.Mesh:
  """Creates a global mesh with the given number of slices.

  Args:
    num_slices: Total number of slices. Used to determine DCN parallelism.
    replica_axis_index: The axis of the replica. Tells emergency checkpointing
      the number of slices. Typically 0, but often 1.
    data_parallelism: For ICI parallelism, the parallelism of the data axis.
    tensor_parallelism: For ICI parallelism, the parallelism of the tensor axis.
    fsdp_parallelism: For ICI parallelism, the parallelism of the fsdp axis.

  Returns:
    A global mesh.
  """
  devices = jax.devices()
  num_devices = len(devices)
  num_devices_per_slice = num_devices // num_slices
  tensor_parallelism = tensor_parallelism or 2
  data_parallelism = data_parallelism or 1
  fsdp_parallelism = fsdp_parallelism or -1

  if num_slices <= 1:
    raise ValueError(f'Must run with at least 2 slices. Found: {num_slices}.')

  mesh_axes = [
      'data',
      'stage',
      'fsdp',
      'fsdp_transpose',
      'sequence',
      'tensor',
      'expert',
      'autoregressive',
  ]
  if replica_axis_index != 0:
    if replica_axis_index == 2 or replica_axis_index == 5:
      raise ValueError(
          '`replica_axis` cannot take the place of `fsdp` or `tensor`.'
      )
    swap_axis_name = mesh_axes[replica_axis_index]
    mesh_axes[replica_axis_index] = 'data'
    mesh_axes[0] = swap_axis_name

  # data_parallelism,
  # pipeline_parallelism,
  # fsdp_parallelism,
  # fsdp_transpose_parallelism,
  # sequence_parallelism,
  # tensor_parallelism,
  # expert_parallelism,
  # autoregressive_parallelism,
  dcn_parallelism = [
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
  ]
  dcn_parallelism[replica_axis_index] = num_slices
  ici_parallelism = [
      1,
      1,
      fsdp_parallelism,
      1,
      1,
      tensor_parallelism,
      1,
      1,
  ]
  ici_parallelism[replica_axis_index] = data_parallelism

  # Find possible unspecified parallelisms
  ici_parallelism = fill_unspecified_mesh_axes(
      ici_parallelism, num_devices_per_slice
  )
  devices_array = mesh_utils.create_hybrid_device_mesh(
      ici_parallelism,
      dcn_parallelism,
      devices,
      allow_split_physical_axes=False,
  )
  logging.info(
      'Creating mesh with axes: %s',
      {axis: dim for axis, dim in zip(mesh_axes, devices_array.shape)},
  )
  return jax.sharding.Mesh(devices_array, mesh_axes)

