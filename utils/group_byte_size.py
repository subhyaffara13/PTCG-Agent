
def GroupByteSize(field_number, message):
  return (2 * TagByteSize(field_number)  # START and END group.
          + message.ByteSize())

