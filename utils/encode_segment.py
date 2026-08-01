
def encode_segment(seg: Segment) -> bytes:
  """Encode a segment into a sequence of VLQs."""
  return b"".join(encode_vlq(value) for value in seg)

