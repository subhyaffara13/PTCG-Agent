import logging
from typing import List

def consistent_restore_mesh(
    devices: List[jax.Device],
    user_mesh: jax.sharding.Mesh,
    previous_flattened_mesh_device_ids: List[int],
    previous_distributed_to_device_ids: List[List[int]],
    current_distributed_to_device_ids: List[List[int]],
):
  """Create a mesh that is consistent with the previous incarnation.

    1. We can think of mesh as being backed by a list of devices.
    2. Default mesh follows the default device id order [0, ..., n-1]. Or
       the user may permute it according to their needs.
    3. After restart, the user will construct the same software mesh as (2).
    4. But a given hardware device may change its id because of scheduler
       or runtime quirks.
    5. Goal: construct the mesh with the same hardware device order as
       before restart, that may not follow the current software ids.
    6. Thus, we shuffle the device order within the mesh by checking how
       each device's software ids changed across restarts.

  This is to restore the same global array values from local hardware devices
  even if software process and device ids have changed across restarts.

  Args:
    devices: List of Jax devices (usually `jax.devices()`).
    user_mesh: The user mesh.
    previous_flattened_mesh_device_ids: The flattened device ids of the mesh.
    previous_distributed_to_device_ids: The distributed id to range of device
      ids mapping of the previous incarnation.
    current_distributed_to_device_ids: The distributed id to range of device ids
      mapping of the current incarnation.

  Returns:
    The new mesh devices that should be used to create the mesh.
  """
  if EXPERIMENTAL_USE_DISTRIBUTED_ID_FOR_MESH_CONSISTENCY.value:
    # Map how device ids changed across restarts.
    device_id_across_restarts = {}
    for i in range(len(previous_distributed_to_device_ids)):
      for j in range(len(previous_distributed_to_device_ids[i])):
        previous_id = previous_distributed_to_device_ids[i][j]
        current_id = current_distributed_to_device_ids[i][j]
        device_id_across_restarts[previous_id] = current_id
    logging.debug(
        'device_id_across_restarts (key: previous_id, value: current_id): %s',
        device_id_across_restarts,
    )
    # Key devices by id.
    jax_devices_by_id = {d.id: d for d in devices}

    new_flattened_mesh_devices = [
        # Convert old ids to current ids that correspond to the same physical
        # hardware.
        jax_devices_by_id[device_id_across_restarts[id]]
        for id in previous_flattened_mesh_device_ids
    ]
    new_mesh_devices = np.array(new_flattened_mesh_devices).reshape(
        user_mesh.devices.shape
    )
  else:
    # This logic assumes jax.devices() returns the same output across restarts.
    # This assumption may break in future Jax releases.
    device_ids = [x.id for x in devices]
    new_flattened_mesh_devices = [
        devices[device_ids.index(i)] for i in previous_flattened_mesh_device_ids
    ]
    new_mesh_devices = np.array(new_flattened_mesh_devices).reshape(
        user_mesh.devices.shape
    )
  return jax.sharding.Mesh(new_mesh_devices, user_mesh.axis_names)

