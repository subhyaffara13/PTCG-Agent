
def normalize_bytes2str(x: bytes) -> str:
  ...


def normalize_bytes2str(x: _T) -> _T:
  ...


def normalize_bytes2str(x):
  """Normalize `bytes` array to `str` (UTF-8).

  Example of usage:

  ```python
  for ex in tfds.as_numpy(ds):  # tf.data returns `tf.string` as `bytes`
    ex = tf.nest.map_structure(enp.normalize_bytes2str, ex)
  ```

  Args:
    x: Any array

  Returns:
    x: `bytes` array are decoded as `str`
  """
  if isinstance(x, str):
    return x
  if isinstance(x, bytes):
    return x.decode('utf8')
  elif is_array_str(x):
    # Note: `np.char.decode` is likely faster but don't work on `object` nor
    # bytes arrays.
    return _to_str_array(x)
  else:
    return x

