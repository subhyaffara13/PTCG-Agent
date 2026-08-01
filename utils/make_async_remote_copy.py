
def make_async_remote_copy(
    src_ref,
    dst_ref,
    send_sem,
    recv_sem,
    device_id: MultiDimDeviceId | IntDeviceId | None,
    device_id_type: primitives.DeviceIdType = primitives.DeviceIdType.MESH,
) -> AsyncCopyDescriptor:
  """Creates a description of a remote copy operation.

  Copies data from src_ref on the current device to dst_ref on the device
  specified by device_id. Both semaphores should be waited on using the
  descriptor on both source and target devices.

  Note that device_id can also refer to the current device.

  Args:
    src_ref: The source Reference.
    dst_ref: The destination Reference.
    send_sem: The semaphore on the source device.
    recv_sem: The semaphore on the destination device.
    device_id: The device id of the destination device. It could be a tuple, or
      a dictionary specifying the communication axis and destination index.
    device_id_type: The type of the device id.

  Returns:
    An AsyncCopyDescriptor.
  """
  if device_id_type == primitives.DeviceIdType.LOGICAL:
    assert not isinstance(
        device_id, tuple | dict
    ), "LOGICAL device_id_type does not support device_id as a tuple or dict."

  return AsyncCopyDescriptor(
      src_ref,
      dst_ref,
      recv_sem,
      send_sem,
      device_id,
      device_id_type=device_id_type,
  )

