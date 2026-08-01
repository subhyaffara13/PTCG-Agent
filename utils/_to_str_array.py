
def _to_str_array(x):
  """Decodes bytes -> str array."""
  # tf.string tensors are returned as bytes, so need to convert them back to str
  return x.decode('utf8') if isinstance(x, bytes) else x

