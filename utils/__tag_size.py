
def _TagSize(field_number):
  """Returns the number of bytes required to serialize a tag with this field
  number."""
  # Just pass in type 0, since the type won't affect the tag+type size.
  return _VarintSize(wire_format.PackTag(field_number, 0))

