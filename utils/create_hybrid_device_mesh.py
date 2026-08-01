
def create_hybrid_device_mesh(
    mesh_shape: Sequence[int],
    dcn_mesh_shape: Sequence[int],
    devices: Sequence[Any] | None = None,
    *,
    process_is_granule: bool = False,
    should_sort_granules_by_key: bool = True,
    allow_split_physical_axes: bool = False,
) -> np.ndarray:
  """Creates a device mesh for hybrid (e.g., ICI and DCN) parallelism.

  Args:
    mesh_shape: shape of the logical mesh for the faster/inner network, ordered
      by increasing network intensity, e.g. [replica, data, mdl] where mdl has
      the most network communication requirements.
    dcn_mesh_shape: shape of the logical mesh for the slower/outer network, in
      the same order as mesh_shape.
    devices: optionally, the devices to construct a mesh for. Defaults to
      jax.devices().
    process_is_granule: if True, this function will treat processes as the units
      of the slower/outer network. Otherwise it will look for slice_index
      attributes on devices and use slices as the units. Enabling this is meant
      as a fallback for platforms that don't set slice_index.
    should_sort_granules_by_key: Whether device granules should be sorted by the
      granule key, either slice or process index, depending on
      process_is_granule.
    allow_split_physical_axes: If True, we will split physical axes if necessary
      to produce the desired device mesh.

  Raises:
    ValueError: if the number of slices to which the `devices` belong doesn't
      equal the product of `dcn_mesh_shape`, or if the number of devices
      belonging to any single slice does not equal the product of `mesh_shape`.

  Returns:
    A np.ndarray of JAX devices with mesh_shape * dcn_mesh_shape as its shape
    that can be fed into jax.sharding.Mesh for hybrid parallelism.
  """
  if devices is None:
    devices = xb.devices()
  attr = 'process_index' if process_is_granule else 'slice_index'
  if not hasattr(devices[0], attr):
    raise ValueError(
        f'Device {devices[0]} does not have attribute {attr}. See'
        ' `process_is_granule` option.'
    )
  granule_dict = collections.defaultdict(list)
  for dev in devices:
    granule_dict[getattr(dev, attr)].append(dev)
  granules = (
      [granule_dict[key] for key in sorted(granule_dict.keys())]
      if should_sort_granules_by_key
      else granule_dict.values()
  )
  if np.prod(dcn_mesh_shape) != len(granules):
    raise ValueError(
        f'Number of slices {len(granules)} must equal the product of '
        f'dcn_mesh_shape {dcn_mesh_shape}'
    )
  per_granule_meshes = [
      create_device_mesh(
          mesh_shape,
          granule,
          allow_split_physical_axes=allow_split_physical_axes,
      )
      for granule in granules
  ]
  # TODO(jekbradbury): handle non-uniform DCN topologies
  granule_mesh = np.arange(len(granules)).reshape(dcn_mesh_shape)
  blocks = np.vectorize(lambda i: per_granule_meshes[i], otypes=[object])(
      granule_mesh
  )
  device_mesh = np.block(blocks.tolist())
  return device_mesh

