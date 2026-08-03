import functools
from typing import Any

def _unreduce_mesh(
    mesh_device_ids: np.ndarray, axis_names: Any, axis_types: Any
) -> jax.sharding.Mesh:
  cpu_device_map = _get_cpu_device_map()
  mesh_devices = np.vectorize(
      functools.partial(_lookup_cpu_device, cpu_device_map)
  )(mesh_device_ids)
  return jax.sharding.Mesh(mesh_devices, axis_names, axis_types)

