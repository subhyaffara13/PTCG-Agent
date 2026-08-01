
def check_tf_result(idx: int, r_tf: TfVal, r_aval: core.ShapedArray | None) -> TfVal:
  # Check that the TF function returns values of expected types. This
  # improves error reporting, preventing hard-to-diagnose errors downstream
  try:
    jax2tf_internal._tfval_to_tensor_jax_dtype(r_tf)
  except Exception as e:
    msg = ("The called TF function returns a result that is not "
           f"convertible to JAX: {r_tf}.")
    raise ValueError(msg) from e

  if r_aval is None:
    return r_tf
  # We convert to TF type, and canonicalize to 32-bit if necessary
  r_aval_dtype_tf = jax2tf_internal._to_tf_dtype(r_aval.dtype)
  # Checking shapes is trickier in presence of dynamic shapes. I wish we could
  # check at runtime that the returned shape matches the declared shape. I wish
  # that tf.ensure_shape did this, but it can only take shapes that contain None
  # not computed shapes. However, in eager mode we should be able to resolve
  # the declared shapes to constants and we get better checking.
  r_aval_shape_tf = jax2tf_internal._aval_to_tf_shape(r_aval)
  # We do as much checking as we can here, instead of relying on tf.ensure_shape
  # because the latter gives different errors in eager vs. compiled mode.
  # TODO(b/279454591): This strange error is from TF. Eager function suppose
  # return tf Val with concrete shape but not.  Here we change exception to warn
  # and bypass it. This case need revisit on TF side.
  try:
    _ = len(r_tf.shape)
  except ValueError as e:
    msg = (
        "The shape check test cannot be performed because the shape of the"
        "`r_tf` tensor cannot be obtained."
        f"r_tf = {r_tf}, r_aval = {r_aval}"
    )
    msg += str(e)
    logging.warning(msg)
    return r_tf
  if (r_tf.dtype != r_aval_dtype_tf or
      len(r_tf.shape) != len(r_aval_shape_tf) or
      any(r_aval_d is not None and r_tf_d is not None and r_aval_d != r_tf_d
          for r_tf_d, r_aval_d in zip(r_tf.shape, r_aval_shape_tf))):
    msg = ("The shapes or dtypes returned by the TensorFlow function "
           "do not match the declared output_shape_dtype:\n"
           f"Result[{idx}] is {r_tf.dtype}[{r_tf.shape}] vs. expected {r_aval_dtype_tf}[{r_aval_shape_tf}]")
    raise ValueError(msg)
  # At this point tf.ensure_shape does not do much, it should never throw an
  # error, albeit it may refine the shape a bit.
  return tf.ensure_shape(r_tf, r_aval_shape_tf)

