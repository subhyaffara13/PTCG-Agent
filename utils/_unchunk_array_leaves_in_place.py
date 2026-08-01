
def _unchunk_array_leaves_in_place(d):
  """Convert chunked array leaves back into array leaves, in place."""
  if isinstance(d, dict):
    if '__msgpack_chunked_array__' in d:
      return _unchunk(d)
    else:
      for k, v in d.items():
        if isinstance(v, dict) and '__msgpack_chunked_array__' in v:
          d[k] = _unchunk(v)
        elif isinstance(v, dict):
          _unchunk_array_leaves_in_place(v)
  return d


def _unchunk_array_leaves_in_place(d):
  """Convert chunked array leaves back into array leaves, in place."""
  if isinstance(d, dict):
    if '__msgpack_chunked_array__' in d:
      return _unchunk(d)
    else:
      for k, v in d.items():
        if isinstance(v, dict) and '__msgpack_chunked_array__' in v:
          d[k] = _unchunk(v)
        elif isinstance(v, dict):
          _unchunk_array_leaves_in_place(v)
  return d

