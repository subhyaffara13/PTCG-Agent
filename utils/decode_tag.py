
def DecodeTag(tag_bytes):
  """Decode a tag from the bytes.

  Args:
    tag_bytes: the bytes of the tag

  Returns:
    Tuple[int, int] of the tag field number and wire type.
  """
  (tag, _) = _DecodeVarint(tag_bytes, 0)
  return wire_format.UnpackTag(tag)

