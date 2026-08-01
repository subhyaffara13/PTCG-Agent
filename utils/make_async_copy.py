
def make_async_copy(src_ref, dst_ref, sem) -> AsyncCopyDescriptor:
  """Creates a description of an asynchronous copy operation.

  Args:
    src_ref: The source Reference.
    dst_ref: The destination Reference.
    sem: The semaphore used to track completion of the copy.

  Returns:
    An AsyncCopyDescriptor.
  """
  return AsyncCopyDescriptor(
      src_ref,
      dst_ref,
      sem,
      None,
      None,
      primitives.DeviceIdType.MESH,
  )

