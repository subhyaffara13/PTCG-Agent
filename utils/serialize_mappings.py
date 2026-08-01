
def serialize_mappings(mappings: Mappings) -> str:
  """Encode mappings into a string of TC39 mapping data."""
  enc = b";".join(
      b",".join(encode_segment(seg) for seg in segs) for segs in mappings
  )
  return enc.decode("ascii")

