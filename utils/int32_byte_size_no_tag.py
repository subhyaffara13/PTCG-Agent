
def Int32ByteSizeNoTag(int32):
  return _VarUInt64ByteSizeNoTag(0xffffffffffffffff & int32)

