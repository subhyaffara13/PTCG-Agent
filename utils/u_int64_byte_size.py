
def UInt64ByteSize(field_number, uint64):
  return TagByteSize(field_number) + _VarUInt64ByteSizeNoTag(uint64)

