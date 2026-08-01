
def TagByteSize(field_number):
  """Returns the bytes required to serialize a tag with this field number."""
  # Just pass in type 0, since the type won't affect the tag+type size.
  return _VarUInt64ByteSizeNoTag(PackTag(field_number, 0))

