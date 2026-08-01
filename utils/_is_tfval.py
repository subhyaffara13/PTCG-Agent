
def _is_tfval(v: TfVal) -> bool:
  if isinstance(v, (tf.Tensor, tf.Variable)):
    return True
  try:
    # Include all convertible types, even if not supported on accelerators.
    with tf.device("CPU"):
      tf.constant(v)
    return True
  except:
    return False

