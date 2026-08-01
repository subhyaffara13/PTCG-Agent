
def _get_none_spec():  # -> tf.TypeSpec:
  """Returns the tf.NoneTensorSpec()."""
  assert lazy.has_tf
  # We need this hack as NoneTensorSpec is not exposed in the public API.
  # (see: b/191132147)
  ds = lazy.tf.data.Dataset.range(0)
  ds = ds.map(lambda x: (x, None))
  return ds.element_spec[-1]

