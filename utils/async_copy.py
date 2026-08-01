
def async_copy(
    src_ref, dst_ref, sem, *, priority: int = 0, add: bool = False,
) -> AsyncCopyDescriptor:
  """Issues a DMA copying from src_ref to dst_ref."""
  copy_descriptor = make_async_copy(src_ref, dst_ref, sem)
  copy_descriptor.start(priority=priority, add=add)
  return copy_descriptor

