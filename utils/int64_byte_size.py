
def Int64ByteSize(field_number, int64):
  # Have to convert to uint before calling UInt64ByteSize().
  return UInt64ByteSize(field_number, 0xffffffffffffffff & int64)

