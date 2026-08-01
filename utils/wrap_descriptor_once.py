
def wrap_descriptor_once(descriptor) -> 'DescriptorWrapper':
  """Wraps a descriptor to give better error messages.

  Args:
    descriptor: User-defined Module attribute descriptor.

  Returns:
    Wrapped descriptor.
  """
  # Don't rewrap descriptors.
  if isinstance(descriptor, DescriptorWrapper):
    return descriptor

  return create_descriptor_wrapper(descriptor)

