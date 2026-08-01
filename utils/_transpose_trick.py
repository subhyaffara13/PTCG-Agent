
def _transpose_trick(
    physical_mesh: np.ndarray, mesh_shape: Sequence[int]
) -> np.ndarray:
  mesh_shape = tuple(mesh_shape)
  topology = physical_mesh.shape
  if topology not in _TRANSPOSE_TRICKS:
    raise ValueError(
        'create_device_mesh cannot create contiguous submeshes for '
        f'physical mesh topology {topology}'
    )

  mesh_shape_no_trivial_dims: tuple[int, ...] = ()
  for dim_size in mesh_shape:
    if dim_size != 1:
      mesh_shape_no_trivial_dims += (dim_size,)

  if mesh_shape_no_trivial_dims not in _TRANSPOSE_TRICKS[topology]:
    raise ValueError(
        'create_device_mesh cannot create contiguous submeshes for '
        f'mesh_shape {mesh_shape} and physical mesh topology {topology}. '
        f'Available mesh_shapes: {list(_TRANSPOSE_TRICKS[topology].keys())}'
    )

  return physical_mesh.transpose(
      *_TRANSPOSE_TRICKS[topology][mesh_shape_no_trivial_dims]
  )

