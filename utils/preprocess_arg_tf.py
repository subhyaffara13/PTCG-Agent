
def preprocess_arg_tf(arg_idx: int,
                      arg_tf: TfVal) -> TfVal:
  """Pre-processes the TF args.

  Returns: a tuple with the pre-processed TF arg, the TF shape, and the
      JAX dtype.
  """
  if not _is_tfval(arg_tf):
    msg = (f"Argument {arg_tf} of type {type(arg_tf)} of jax2tf.convert(f) should "
           "be NumPy array, scalar, tf.Variable, or tf.Tensor")
    raise TypeError(msg)

  # May cast the args_flat to JAX types, using JAX's interpretation
  # of types of constants.
  arg_tf, _ = _tfval_to_tensor_jax_dtype(arg_tf)
  # Name input tensors; do this after we have cast the arguments
  arg_tf = tf.identity(arg_tf, f"jax2tf_arg_{arg_idx}")
  return arg_tf

