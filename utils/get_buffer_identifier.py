
def GetBufferIdentifier(buf, offset, size_prefixed=False):
  """Extract the file_identifier from a buffer"""
  if size_prefixed:
    # increase offset by size of UOffsetTFlags
    offset += number_types.UOffsetTFlags.bytewidth
  # increase offset by size of root table pointer
  offset += number_types.UOffsetTFlags.bytewidth
  # end of FILE_IDENTIFIER
  end = offset + encode.FILE_IDENTIFIER_LENGTH
  return buf[offset:end]

