from typing import Any

def install_pathways_colocated_serialization_patch() -> None:
  """Installs a Pathways-aware colocated-python serialization patch.

  The live Pathways failures are below Orbax checkpoint semantics. They happen
  while JAX is pickling and unpickling callable specializations that contain
  mesh-backed shardings.

  The patch is intentionally narrow:

  1. Keep JAX's existing serialized representation based on integer CPU ids
  2. Normalize any non-CPU mesh/device-list/sharding to colocated CPU devices
     before it reaches JAX's reducers
  3. Teach worker-side CPU lookup to recognize backend-global PjRt-IFRT ids,
     which are what controller-side CPU `device.id` values correspond to in the
     Pathways remote-Python runtime

  This keeps Orbax close to upstream JAX semantics while fixing the exact
  controller/proxy/worker identity mismatch seen in Pathways logs.

  The important constraint is that we are not changing the checkpoint contract
  or inventing a second serialized format. We are only making JAX's existing
  colocated serialization contract portable across the controller/worker CPU-id
  namespace split used by Pathways single-controller.

  Tracked at b/503051746 to make proper changes to JAX.
  """
  # pylint: disable=global-statement
  global _PATHWAYS_SERIALIZATION_PATCH_INSTALLED
  if _PATHWAYS_SERIALIZATION_PATCH_INSTALLED:
    return

  original_reduce_mesh = cp_serialization._reduce_mesh  # pylint: disable=protected-access
  original_reduce_device_list = cp_serialization._reduce_device_list  # pylint: disable=protected-access
  original_reduce_single_device_sharding = cp_serialization._reduce_single_device_sharding  # pylint: disable=protected-access

  def _orbax_reduce_mesh(mesh: jax.sharding.Mesh) -> Any:
    return original_reduce_mesh(_normalize_mesh_to_colocated_cpu(mesh))

  def _orbax_reduce_device_list(
      device_list: cp_serialization.DeviceList,
  ) -> Any:
    return original_reduce_device_list(
        _normalize_device_list_to_colocated_cpu(device_list)
    )

  def _orbax_reduce_single_device_sharding(
      sharding: jax.sharding.SingleDeviceSharding,
  ) -> Any:
    return original_reduce_single_device_sharding(
        _normalize_single_device_sharding_to_colocated_cpu(sharding)
    )

  cp_serialization._reduce_mesh = _orbax_reduce_mesh  # pylint: disable=protected-access
  cp_serialization._reduce_device_list = _orbax_reduce_device_list  # pylint: disable=protected-access
  cp_serialization._reduce_single_device_sharding = _orbax_reduce_single_device_sharding  # pylint: disable=protected-access
  cp_serialization._get_cpu_device_map = _get_cpu_device_map  # pylint: disable=protected-access
  _PATHWAYS_SERIALIZATION_PATCH_INSTALLED = True

