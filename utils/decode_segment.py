
def decode_segment(enc: Iterable[int]) -> Segment:
  """Decode a sequence of VLQs into a segment."""
  enc_iter = iter(enc)
  col = decode_vlq(enc_iter)
  try:
    source = decode_vlq(enc_iter)
  except StopIteration:
    # Stopping here is fine (1-segment).
    return (col,)
  source_line = decode_vlq(enc_iter)
  source_col = decode_vlq(enc_iter)
  try:
    name = decode_vlq(enc_iter)
  except StopIteration:
    # Stopping here is fine too (4-segment).
    return col, source, source_line, source_col
  # (5-segment)
  return col, source, source_line, source_col, name

