
def MessageSetItemByteSize(field_number, msg):
  # First compute the sizes of the tags.
  # There are 2 tags for the beginning and ending of the repeated group, that
  # is field number 1, one with field number 2 (type_id) and one with field
  # number 3 (message).
  total_size = (2 * TagByteSize(1) + TagByteSize(2) + TagByteSize(3))

  # Add the number of bytes for type_id.
  total_size += _VarUInt64ByteSizeNoTag(field_number)

  message_size = msg.ByteSize()

  # The number of bytes for encoding the length of the message.
  total_size += _VarUInt64ByteSizeNoTag(message_size)

  # The size of the message.
  total_size += message_size
  return total_size

