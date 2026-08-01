
def BufferHasIdentifier(buf, offset, file_identifier, size_prefixed=False):
  got = GetBufferIdentifier(buf, offset, size_prefixed=size_prefixed)
  return got == file_identifier

