
def make_mesh(
    topo: TopologyDescription,
    mesh_shape: Sequence[int],
    axis_names: tuple[str, ...],
    *,
    contiguous_submeshes: bool = False
) -> jax.sharding.Mesh:
  devices = mesh_utils.create_device_mesh(
      mesh_shape, list(topo.devices), contiguous_submeshes=contiguous_submeshes)
  return jax.sharding.Mesh(devices, axis_names)


def make_mesh(axis_shapes: Sequence[int], axis_names: Sequence[str],
              axis_types: tuple[AxisType, ...] | None = None,
              *, devices: Sequence[xc.Device] | None = None) -> Mesh:
  """Creates an efficient mesh with the shape and axis names specified.

  This function attempts to automatically compute a good mapping from a set of
  logical axes to a physical mesh. For example, on a TPU v3 with 8 devices:

  >>> mesh = jax.make_mesh((8,), ('x'))  # doctest: +SKIP
  >>> [d.id for d in mesh.devices.flat]  # doctest: +SKIP
  [0, 1, 2, 3, 6, 7, 4, 5]

  The above ordering takes into account the physical topology of TPU v3.
  It orders the devices into a ring, which yields efficient all-reduces on a
  TPU v3.

  Now, let's see another example with 16 devices of TPU v3:

  >>> mesh = jax.make_mesh((2, 8), ('x', 'y'))  # doctest: +SKIP
  >>> [d.id for d in mesh.devices.flat]  # doctest: +SKIP
  [0, 1, 2, 3, 6, 7, 4, 5, 8, 9, 10, 11, 14, 15, 12, 13]
  >>> mesh = jax.make_mesh((4, 4), ('x', 'y'))  # doctest: +SKIP
  >>> [d.id for d in mesh.devices.flat]  # doctest: +SKIP
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

  As you can see, logical axes (`axis_shapes`) affect the ordering of the
  devices.

  You can use `jax.experimental.mesh_utils.create_device_mesh` if you want to
  use the extra arguments it provides like `contiguous_submeshes` and
  `allow_split_physical_axes`.

  Args:
    axis_shapes: Shape of the mesh. For example, axis_shape=(4, 2)
    axis_names: Names of the mesh axes. For example, axis_names=('x', 'y')
    axis_types: Optional tuple of :class:`jax.sharding.AxisType` entries
      corresponding to the ``axis_names``. See `Explicit Sharding`_ for more
      information.
    devices: Optional keyword only argument, that allows you to specify the
      devices you want to create a mesh with.

  Returns:
    A :class:`jax.sharding.Mesh` object.

  .. _Explicit Sharding:  https://docs.jax.dev/en/latest/parallel.html
  """
  if devices is None:
    devices = xb.devices()
  new_axis_shapes = mesh_utils._canonicalize_axis_sizes(axis_shapes)
  if new_axis_shapes is None:
    raise ValueError(
        '`axis_shapes` passed to `make_mesh` should be a sequence of ints.'
        f' Got {axis_shapes}')
  del axis_shapes

  axis_size = math.prod(new_axis_shapes)
  if axis_size > len(devices):
    raise ValueError(
        f'Number of devices {len(devices)} must be >= the product '
        f'of mesh_shape {new_axis_shapes}')
  elif axis_size < len(devices):
    devices = devices[:axis_size]
  if devices[0].device_kind in (mesh_utils._TPU_V5_LITE, mesh_utils._TPU_V5E):
    allow_split_physical_axes = True
  else:
    allow_split_physical_axes = False
  mesh_devices = mesh_utils.create_device_mesh(
      new_axis_shapes, devices,
      allow_split_physical_axes=allow_split_physical_axes)
  if (hasattr(mesh_devices.flat[0], 'slice_index') and
      len({d.slice_index for d in mesh_devices.flat}) > 1):
    raise ValueError(
        '`jax.make_mesh` does not support multi-slice topologies. Please use'
        ' jax.experimental.mesh_utils.create_hybrid_device_mesh')
  if axis_types is None:
    axis_types = (AxisType.Explicit,) * len(mesh_devices.shape)
  return Mesh(mesh_devices, axis_names, axis_types=axis_types)

