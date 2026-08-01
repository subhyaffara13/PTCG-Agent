
def _InternalUnpackAny(msg):
  """Unpacks Any message and returns the unpacked message.

  This internal method is different from public Any Unpack method which takes
  the target message as argument. _InternalUnpackAny method does not have
  target message type and need to find the message type in descriptor pool.

  Args:
    msg: An Any message to be unpacked.

  Returns:
    The unpacked message.
  """
  # TODO: Don't use the factory of generated messages.
  # To make Any work with custom factories, use the message factory of the
  # parent message.
  # pylint: disable=g-import-not-at-top
  from google.protobuf import symbol_database
  factory = symbol_database.Default()

  type_url = msg.type_url

  if not type_url:
    return None

  # TODO: For now we just strip the hostname.  Better logic will be
  # required.
  type_name = type_url.split('/')[-1]
  descriptor = factory.pool.FindMessageTypeByName(type_name)

  if descriptor is None:
    return None

  # Unable to import message_factory at top because of circular import.
  # pylint: disable=g-import-not-at-top
  from google.protobuf import message_factory
  message_class = message_factory.GetMessageClass(descriptor)
  message = message_class()

  message.ParseFromString(msg.value)
  return message

