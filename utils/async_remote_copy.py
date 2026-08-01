
def async_remote_copy(
    src_ref,
    dst_ref,
    send_sem,
    recv_sem,
    device_id,
    device_id_type: primitives.DeviceIdType = primitives.DeviceIdType.MESH,
) -> AsyncCopyDescriptor:
  """Issues a remote DMA copying from src_ref to dst_ref."""
  copy_descriptor = make_async_remote_copy(src_ref, dst_ref, send_sem, recv_sem,
                                           device_id, device_id_type)
  copy_descriptor.start()
  return copy_descriptor

