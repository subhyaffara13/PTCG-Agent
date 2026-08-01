
def BytesByteSize(field_number, b):
  return (TagByteSize(field_number)
          + _VarUInt64ByteSizeNoTag(len(b))
          + len(b))

