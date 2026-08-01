
def byte_size(message: Message) -> int:
  """Returns the serialized size of this message.

  Args:
    message: A proto message.

  Returns:
    int: The number of bytes required to serialize this message.
  """
  return message.ByteSize()

