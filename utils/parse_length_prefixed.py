
def parse_length_prefixed(
    message_class: Type[_MESSAGE], input_bytes: io.BytesIO
) -> _MESSAGE:
  """Parse a message from input_bytes.

  Args:
    message_class: The protocol buffer message class that parser should parse.
    input_bytes: A buffered input.

  Example usage:
    while True:
      msg = proto.parse_length_prefixed(message_class, input_bytes)
      if msg is None:
        break
      ...

  Returns:
    A parsed message if successful. None if input_bytes is at EOF.
  """
  size = decoder._DecodeVarint(input_bytes)
  if size is None:
    # It is the end of buffered input. See example usage in the
    # API description.
    return None

  message = message_class()

  if size == 0:
    return message

  parsed_size = message.ParseFromString(input_bytes.read(size))
  if parsed_size != size:
    raise ValueError(
        'Truncated message or non-buffered input_bytes: '
        'Expected {0} bytes but only {1} bytes parsed for '
        '{2}.'.format(size, parsed_size, message.DESCRIPTOR.name)
    )
  return message

