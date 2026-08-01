
def _tpu_v2_v3_create_device_mesh(
    mesh_shape: Sequence[int],
    devices: Sequence[Any],
    **unused_kwargs,
) -> np.ndarray:
  if len(devices) == 8:
    device_mesh = np.asarray(devices)
    device_mesh = device_mesh[np.array(_TRAY_RING_ORDER)]
    device_mesh = device_mesh.reshape(mesh_shape)
    return device_mesh
  elif mesh_shape[-1] == 8:
    device_mesh = np.asarray(devices).reshape(mesh_shape)
    perm = np.array(_TRAY_RING_ORDER)
    device_mesh = device_mesh[..., perm]
    return device_mesh
  else:
    # TODO(skye): implement 2D mesh_shape logic here:
    # https://github.com/tensorflow/lingvo/blob/0df40cf604dfcd14e28f7087d73687a0bd2fe5c6/lingvo/core/gshard_utils.py#L187
    # (possibly replaces above mesh_shape[-1] == 8 case)
    return np.asarray(devices).reshape(mesh_shape)

