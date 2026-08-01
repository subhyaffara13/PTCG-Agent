
def dtype_of_val(val: TfVal) -> DType:
  """Computes the TensorFlow dtype using JAX's typing rules.

  If the value is a tf.Tensor, it starts with its dtype. If the value is a
  constant it uses JAX to infer its dtype. The resulting dtype follows the
  JAX type inference rules, and depends on the value of the
  JAX_ENABLE_X64 flag.

  See README.md for how 64-bit values are treated.
  """
  tval, _ = _tfval_to_tensor_jax_dtype(val)
  return tval.dtype

