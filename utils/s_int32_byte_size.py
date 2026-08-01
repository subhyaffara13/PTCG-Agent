
def SInt32ByteSize(field_number, int32):
  return UInt32ByteSize(field_number, ZigZagEncode(int32))

