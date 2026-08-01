
def _call_tf_impl(*args_jax_flat, callable_flat_tf, **_):
  # On GPU we use dlpack to avoid copies of data to the host.
  def _arg_jax_to_tf(arg_jax):
    if (isinstance(arg_jax, jax.Array) and
        list(arg_jax.devices())[0].platform in _DLPACK_PLATFORMS and
        dlpack.is_supported_dtype(arg_jax.dtype)):
      return tf.experimental.dlpack.from_dlpack(arg_jax.__dlpack__())
    # The following avoids copies to the host on CPU, always for Array
    # and even for ndarray if they are sufficiently aligned.
    # TODO(necula): on TPU this copies to the host!
    if getattr(arg_jax, 'dtype', None) == dtypes.float0:
      return tf.zeros(shape=arg_jax.shape,
                      dtype=jax2tf_internal._tf_np_dtype_for_float0)
    if isinstance(arg_jax, tuple(literals.typed_scalar_types)):
      # Make sure to preserve the JAX dtype for TypedInt, etc.
      return tf.constant(np.asarray(arg_jax, dtype=arg_jax.dtype))
    return tf.constant(np.asarray(arg_jax))

  args_tf_flat = tuple(map(_arg_jax_to_tf, args_jax_flat))
  with jax2tf_internal.inside_call_tf():
    # Call in TF eager mode
    res_tf_flat = callable_flat_tf(*args_tf_flat)

  def _res_tf_to_jax(res_tf: TfVal):
    res_tf, jax_dtype = jax2tf_internal._tfval_to_tensor_jax_dtype(res_tf)
    if isinstance(res_tf, tf.Tensor) and dlpack.is_supported_dtype(jax_dtype):
      res_tf_platform = tf.DeviceSpec.from_string(res_tf.backing_device).device_type
      res_jax_platform = res_tf_platform.lower()
      if res_jax_platform in _DLPACK_PLATFORMS:
        return jax.dlpack.from_dlpack(res_tf)

    # When working with a bfloat16 scalar tf.Tensor,np.asarray() can fail.
    # To handle this special case, we create a numpy copy.
    if res_tf.shape == tf.TensorShape([]) and res_tf.dtype == tf.bfloat16:
      return jax.device_put(jnp.array(res_tf.numpy()))
    else:
      return jax.device_put(np.asarray(res_tf))

  return list(map(_res_tf_to_jax, res_tf_flat))

