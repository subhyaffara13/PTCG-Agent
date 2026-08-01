
def _BuildMessageFromTypeName(type_name, descriptor_pool):
  """Returns a protobuf message instance.

  Args:
    type_name: Fully-qualified protobuf  message type name string.
    descriptor_pool: DescriptorPool instance.

  Returns:
    A Message instance of type matching type_name, or None if the a Descriptor
    wasn't found matching type_name.
  """
  # pylint: disable=g-import-not-at-top
  if descriptor_pool is None:
    from google.protobuf import descriptor_pool as pool_mod

    descriptor_pool = pool_mod.Default()
  from google.protobuf import message_factory

  try:
    message_descriptor = descriptor_pool.FindMessageTypeByName(type_name)
  except KeyError:
    return None
  message_type = message_factory.GetMessageClass(message_descriptor)
  return message_type()

