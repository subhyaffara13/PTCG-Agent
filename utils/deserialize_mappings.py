
def deserialize_mappings(mappings_str: str) -> Mappings:
  """Decode a string of TC39 mapping data."""
  mappings_bytes = bytes(mappings_str, encoding="ascii")
  return [
      list(map(decode_segment, mapping.split(b","))) if mapping else []
      for mapping in mappings_bytes.split(b";")
  ]

