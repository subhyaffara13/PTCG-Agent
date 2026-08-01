
def _unchunk(data: dict[str, Any]):
  """Convert canonical dictionary of chunked arrays back into array."""
  assert '__msgpack_chunked_array__' in data
  shape = _dict_to_tuple(data['shape'])
  flatarr = np.concatenate(_dict_to_tuple(data['chunks']))
  return flatarr.reshape(shape)


def _unchunk(data: Dict[str, Any]):
  """Convert canonical dictionary of chunked arrays back into array."""
  assert '__msgpack_chunked_array__' in data
  shape = _dict_to_tuple(data['shape'])
  flatarr = np.concatenate(_dict_to_tuple(data['chunks']))
  return flatarr.reshape(shape)

