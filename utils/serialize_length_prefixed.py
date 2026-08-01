
def serialize_length_prefixed(message: _MESSAGE, output: io.BytesIO) -> None:
  """Writes the size of the message as a varint and the serialized message.

  Writes the size of the message as a varint and then the serialized message.
  This allows more data to be written to the output after the message. Use
  parse_length_prefixed to parse messages written by this method.

  The output stream must be buffered, e.g. using
  https://docs.python.org/3/library/io.html#buffered-streams.

  Example usage:
    out = io.BytesIO()
    for msg in message_list:
      proto.serialize_length_prefixed(msg, out)

  Args:
    message: The protocol buffer message that should be serialized.
    output: BytesIO or custom buffered IO that data should be written to.
  """
  size = message.ByteSize()
  encoder._VarintEncoder()(output.write, size)
  out_size = output.write(serialize(message))

  if out_size != size:
    raise TypeError(
        'Failed to write complete message (wrote: %d, expected: %d)'
        '. Ensure output is using buffered IO.' % (out_size, size)
    )

