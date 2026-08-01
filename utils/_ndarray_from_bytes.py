
def _ndarray_from_bytes(data: bytes) -> np.ndarray:
  """Load ndarray from simple msgpack encoding."""
  shape, dtype_name, buffer = msgpack.unpackb(data, raw=True)
  return np.frombuffer(
    buffer, dtype=_dtype_from_name(dtype_name), count=-1, offset=0
  ).reshape(shape, order='C')


def _ndarray_from_bytes(data: bytes) -> np.ndarray:
  """Load ndarray from simple msgpack encoding."""
  shape, dtype_name, buffer = msgpack.unpackb(data, raw=True)
  return np.frombuffer(buffer,
                       dtype=_dtype_from_name(dtype_name),
                       count=-1,
                       offset=0).reshape(shape, order='C')

