
def _CheckFieldMaskMessage(message):
  """Raises ValueError if message is not a FieldMask."""
  message_descriptor = message.DESCRIPTOR
  if (message_descriptor.name != 'FieldMask' or
      message_descriptor.file.name != 'google/protobuf/field_mask.proto'):
    raise ValueError('Message {0} is not a FieldMask.'.format(
        message_descriptor.full_name))

