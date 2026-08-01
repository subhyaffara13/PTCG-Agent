
def MessageByteSize(field_number, message):
  return (TagByteSize(field_number)
          + _VarUInt64ByteSizeNoTag(message.ByteSize())
          + message.ByteSize())

