
def make_array_from_process_local_data(
    sharding,  # PyTree[jax.sharding.Sharding]
    local_data,  # PyTree[np.ndarray]
    global_shape=None):  # PyTree[Shape]
  # pyformat: disable
  """Creates distributed tensor using the data available in process.

  This function is a common special case of `make_array_from_callback`. It
  assumes that the data is available in the process and takes care of the
  index wrangling.

  The most common case is when the sharding is sharded across the batch
  dimension and each host just loads its corresponding sub-batch. This function
  supports more general cases as well, such as mixed multi-host and multi-axis
  replication and sharding but you would need to compute the size and the
  contents of process-local data correctly to satisfy the sharding constraints.

  In particular, if any two hosts are replicas, host_local_data should be
  identical as well.

  The global_shape is optional. If not provided it will be be inferred from
  the local_data and sharding, under the assumption that
  each host represents only their own data for uniform sharding. If sharding
  is non-uniform, (see note below) an exception will be raised.

  Setting global_shape explicitly allows for finer grain control and works with
  non-uniform shardings. Each dimension of global_shape must either match
  host_local_data, or match the inferred global shape of the sharding (in which
  case it is equivalent to setting it to None, but is more explicit).

  For example if dimension `i` is fully sharded then this size would be
  `per_device_shape[i] * jax.local_device_count()`.  Each device will be mapped
  into local slice of `local_data` array. For example, if given process
  addresses slices (8, 12) and  (24, 28), then these slices will be mapped
  into (0, 4) and (4, 8) of the `local_data`.

  For each dimension where global_shapes matches local_shape, each device
  will lookup the slice in the local_data. For example if
  global_shape == local_data.shape, the local data is assumed to be the
  actual target array that will be sharded into device.

  If global_shape is the same as local_data.shape, then the data must
  be the same across all hosts.

  Examples:
    >>> from jax.sharding import PartitionSpec as P
    >>> mesh_rows = 2
    >>> mesh_cols =  jax.device_count() // 2
    ...
    >>> mesh = jax.sharding.Mesh(np.array(jax.devices()).reshape(mesh_rows, mesh_cols), ('x', 'y'))

    >>> sharding = jax.sharding.NamedSharding(mesh, P(('x', 'y'),))
    >>> rows_per_device = 2
    >>> feature_length = 32
    >>> per_device_shape = (rows_per_device, feature_length)
    >>> per_host_shape = (rows_per_device * len(mesh.local_devices), feature_length)
    >>> per_host_generator = lambda : np.arange(np.prod(per_host_shape)).reshape(per_host_shape)
    >>> per_host_data = per_host_generator()  # replace with your own per-host data pipeline that outputs numpy arrays
    >>> global_shape = (rows_per_device * len(sharding.device_set), ) + per_device_shape[1:]
    >>> output_global_array = jax.make_array_from_process_local_data(sharding, per_host_data, global_shape)
    ...
    >>> assert output_global_array.addressable_data(0).shape == per_device_shape
    >>> assert output_global_array.shape == global_shape

  NB: While most shardings are uniform, It is possible to design an exotic
  sharding mesh where each process's  devices will be arranged in a non-grid
  like pattern in some dimensions, or for indices to overlap non-trivially.
  Such sharding is called "non-uniform" in those dimensions. In that case,
  the global shape along those directions must match local shape as there is
  no meaningful way to represent all needed
  per-process data in non-overlapping fashion. For example for global_shape 4x4
  if sharding looks like this::

      0123
      2103
      4675
      4567

  with 4 processes, containing devices (0,1), (2, 3), (4, 5), (6, 7) respectively.
  Then the data for each host look like::

      xx..    ..xx     ....    ....
      .xx.    x..x     ....    ....
      ....    ....     x..x    .xx.
      ....    ....     xx..    ..xx

  the sharding is uniform on rows (each host requires either rows 1-2, or rows 3-4)
  and non-uniform on columns (hosts require overlapping but not matching
  set of columns). Thus local data must have the shape 2x4 or 4x4
  for all hosts, even though each  host can potentially fit into 2x2 shape.
  In this case user must provide global_shape explicitly and for
  local_shape=(2, 4), potentially valid global shapes are (2, 4) and (4, 4).

  On the other hand for sharding::

      0213   x.x.  .x.x.  ....  ....
      0213   x.x.  .x.x.  ....  ....
      4657   ....  ....   .x.x  x.x.
      4657   ....  ....   .x.x  x.x.

  for local_shape=(2, 2) this function can accept a choice of 2x2, 2x4, 4x2
  and 4x4 global shapes. Setting global_shape to None, is equivalent to
  setting it to (4, 4) in this case.

  Args:
    sharding: Sharding of the global array.
    local_data: Data on the host to be placed on local devices. Each
      dimension should either match global_shape, or match
      num_addressable_indices(dim).
    global_shape: The target shape of the global array. If None,
      will infer from local_data and sharding.

  Returns:
    Tensor that will have sharding=sharding and of shape global_shape.
  """
  # pyformat: enable
  local_data_flat, treedef = tree_flatten(local_data)
  sharding_flat = broadcast_prefix(sharding, local_data)
  sharding_flat = map(
      partial(api.pspec_to_sharding, 'make_array_from_process_local_data'),
      sharding_flat)
  global_shape_flat = broadcast_prefix(
      global_shape, local_data,
      is_leaf=lambda x: x is None or isinstance(x, tuple))
  if xla_bridge.process_count() == 1:
    # Safety check if the provided data doesn't match expected global_shape
    for s, d in zip(global_shape_flat, local_data_flat):
      if s is not None and s != d.shape:
        raise ValueError(
            "When calling `make_array_from_process_local_data` on a single"
            " process, global_shape should be None or equal to"
            f" local_data.shape.Got global_shape={s} and"
            f" local_data.shape={d.shape}."
        )
    return api.device_put(local_data, sharding)

  out = [_array_from_process_local_data(data, s, shape)
         for data, s, shape in zip(local_data_flat, sharding_flat, global_shape_flat)]
  return tree_unflatten(treedef, out)

