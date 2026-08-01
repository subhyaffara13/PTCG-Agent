
def create_device_mesh(
    mesh_shape: Sequence[int],
    devices: Sequence[Any] | None = None,
    *,
    contiguous_submeshes: bool = False,
    allow_split_physical_axes: bool = False,
) -> np.ndarray:
  """Creates a performant device mesh for jax.sharding.Mesh.

  Args:
    mesh_shape: shape of logical mesh, ordered by increasing network-intensity
      e.g. [replica, data, mdl] where mdl has the most network communication
      requirements.
    devices: optionally, the devices to construct a mesh for. Defaults to
      jax.devices().
    contiguous_submeshes: if True, this function will attempt to create a mesh
      where each process's local devices form a contiguous submesh. A ValueError
      will be raised if this function can't produce a suitable mesh. This
      setting was sometimes necessary before the introduction of jax.Array to
      ensure non-ragged local arrays; if using jax.Arrays, it's better to keep
      this set to False.
    allow_split_physical_axes: If True, we will split physical axes if necessary
      to produce the desired device mesh.

  Raises:
    ValueError: if the number of devices doesn't equal the product of
      `mesh_shape`.

  Returns:
    A np.ndarray of JAX devices with mesh_shape as its shape that can be fed
    into jax.sharding.Mesh with good collective performance.
  """
  if devices is None:
    devices = xb.devices()

  new_mesh_shape = _canonicalize_axis_sizes(mesh_shape)
  if new_mesh_shape is None:
    raise ValueError(
        f'`mesh_shape` passed to `create_device_mesh` should be a sequence of'
        f' ints. Got {mesh_shape}')
  del mesh_shape

  if math.prod(new_mesh_shape) != len(devices):
    raise ValueError(
        f'Number of devices {len(devices)} must equal the product '
        f'of mesh_shape {new_mesh_shape}'
    )
  last_device = devices[-1]

  handler = device_kind_handler_dict.get(last_device.device_kind, None)
  if handler is not None:
    result = handler(
        new_mesh_shape, devices, contiguous_submeshes=contiguous_submeshes
    )
    if result is not None:
      return result

  if last_device.platform == 'tpu':
    physical_mesh = _get_physical_tpu_mesh(devices)
    if contiguous_submeshes:
      physical_mesh = _transpose_trick(physical_mesh, new_mesh_shape)
    device_mesh, _ = _create_device_mesh_for_nd_torus(
        physical_mesh,
        new_mesh_shape,
        allow_split_physical_axes=allow_split_physical_axes,
    )
    return device_mesh
  elif last_device.platform == 'gpu':
    # The default jax.devices() order is not guaranteed to be performant, as it is
    # based on process order rather than the topology-aware global numbering scheme
    # assigned by XLA. If the device list is single-slice, this does not matter on
    # modern systems, but the sort avoids a sharp edge if a multi-slice device list
    # is passed.
    return np.asarray(sorted(devices, key=lambda d: d.id)).reshape(new_mesh_shape)
  else:
    device_mesh = np.asarray(devices).reshape(new_mesh_shape)
    return device_mesh

