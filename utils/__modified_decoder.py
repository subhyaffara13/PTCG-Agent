
def _ModifiedDecoder(wire_type, decode_value, modify_value):
  """Like SimpleDecoder but additionally invokes modify_value on every value
  before storing it.  Usually modify_value is ZigZagDecode.
  """

  # Reusing _SimpleDecoder is slightly slower than copying a bunch of code, but
  # not enough to make a significant difference.

  def InnerDecode(buffer, pos):
    (result, new_pos) = decode_value(buffer, pos)
    return (modify_value(result), new_pos)
  return _SimpleDecoder(wire_type, InnerDecode)

