
def _chunk(arr) -> dict[str, Any]:
  """Convert array to a canonical dictionary of chunked arrays."""
  chunksize = max(1, int(MAX_CHUNK_SIZE / arr.dtype.itemsize))
  data = {'__msgpack_chunked_array__': True, 'shape': _tuple_to_dict(arr.shape)}
  flatarr = arr.reshape(-1)
  chunks = [
    flatarr[i : i + chunksize] for i in range(0, flatarr.size, chunksize)
  ]
  data['chunks'] = _tuple_to_dict(chunks)
  return data


def _chunk(arr) -> Dict[str, Any]:
  """Convert array to a canonical dictionary of chunked arrays."""
  chunksize = max(1, int(MAX_CHUNK_SIZE / arr.dtype.itemsize))
  data = {'__msgpack_chunked_array__': True,
          'shape': _tuple_to_dict(arr.shape)}
  flatarr = arr.reshape(-1)
  chunks = [flatarr[i:i + chunksize] for i in range(0, flatarr.size, chunksize)]
  data['chunks'] = _tuple_to_dict(chunks)
  return data

