
def make_vlq_decode_table():
  lookup = {c: d for d, c in enumerate(VLQ_ALPHABET)}
  return [lookup.get(i, None) for i in range(256)]

