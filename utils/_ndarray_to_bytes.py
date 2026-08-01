
def _ndarray_to_bytes(arr) -> bytes:
  """Save ndarray to simple msgpack encoding."""
  if isinstance(arr, jax.Array):
    arr = np.array(arr)
  if arr.dtype.hasobject or arr.dtype.isalignedstruct:
    raise ValueError(
      'Object and structured dtypes not supported '
      'for serialization of ndarrays.'
    )
  tpl = (arr.shape, arr.dtype.name, arr.tobytes('C'))
  return msgpack.packb(tpl, use_bin_type=True)


def _ndarray_to_bytes(arr) -> bytes:
  """Save ndarray to simple msgpack encoding."""
  if isinstance(arr, jax.Array):
    arr = np.array(arr)
  if arr.dtype.hasobject or arr.dtype.isalignedstruct:
    raise ValueError('Object and structured dtypes not supported '
                     'for serialization of ndarrays.')
  tpl = (arr.shape, arr.dtype.name, arr.tobytes('C'))
  return msgpack.packb(tpl, use_bin_type=True)

