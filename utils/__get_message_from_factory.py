
def _GetMessageFromFactory(pool, full_name):
  """Get a proto class from the MessageFactory by name.

  Args:
    pool: a descriptor pool.
    full_name: str, the fully qualified name of the proto type.
  Returns:
    A class, for the type identified by full_name.
  Raises:
    KeyError, if the proto is not found in the factory's descriptor pool.
  """
  proto_descriptor = pool.FindMessageTypeByName(full_name)
  proto_cls = message_factory.GetMessageClass(proto_descriptor)
  return proto_cls

