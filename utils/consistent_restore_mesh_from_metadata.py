import logging
from typing import List

def consistent_restore_mesh_from_metadata(
    global_mesh: jax.sharding.Mesh,
    current_distributed_to_device_ids: List[List[int]],
    previous_distributed_to_device_ids: List[List[int]],
    previous_device_ids: List[int],
) -> jax.sharding.Mesh:
  """Create a mesh consistent with the saved metadata.

  Each device has its own specific local shard.
  Naive example:
    Before restart: device X (with id 0) saves shard 0.
    After restart:  device X (with new id 1) reads shard 0.
  To ensure the same device X (with different software ids) reads the
  same locally available shard and represent it in the correct index
  within the global jax.Array, we use the `restore_mesh`.

  More context on `restore_mesh`:
  1. We can think of mesh as being backed by a list of devices.
  2. Default mesh follows the default device id order [0, ..., n-1]. Or
      the user may permute it according to their needs.
  3. After restart, the user will construct the same software mesh as (2).
  4. But a given hardware device may change its id because of scheduler
      or runtime quirks.
  5. Goal: construct the mesh with the same hardware device order as
      before restart, that may not follow the current software ids.
  5. Thus, we shuffle the device order within the mesh by checking how
      each device's software ids changed across restarts.

  Args:
    global_mesh: The global mesh, provided by the user.
    current_distributed_to_device_ids: The distributed id to range of device ids
      mapping of the current incarnation.
    previous_distributed_to_device_ids: The distributed id to range of device
      ids mapping of the previous incarnation.
    previous_device_ids: The device ids of the previous incarnation.

  Returns:
    A mesh that is the same as the mesh used to save the local checkpoint.
  """
  assert isinstance(previous_device_ids, list)
  logging.info(
      'From process metadata, distributed_to_device_ids=%s',
      previous_distributed_to_device_ids,
  )
  logging.info('From process metadata, device_ids=%s', previous_device_ids)
  consistent_mesh = emergency_multihost.consistent_restore_mesh(
      jax.devices(),
      global_mesh,
      previous_device_ids,
      previous_distributed_to_device_ids=previous_distributed_to_device_ids,
      current_distributed_to_device_ids=current_distributed_to_device_ids,
  )
  logging.info(
      'Created consistent mesh with device_ids=%s',
      consistent_mesh.device_ids.flatten(),
  )
  return consistent_mesh

