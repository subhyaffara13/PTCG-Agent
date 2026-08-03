from typing import Any

def _v4i_v8i_create_device_mesh(
    mesh_shape: Sequence[int], devices: Sequence[Any], **unused_kwargs
) -> np.ndarray | None:
  if len(devices) == 4:
    device_mesh = np.asarray(devices)
    device_mesh = device_mesh[np.array(_TRAY_2x2_RING_ORDER)]
    device_mesh = device_mesh.reshape(mesh_shape)
    return device_mesh
  return None

