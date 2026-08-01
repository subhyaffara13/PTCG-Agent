
def _tfval_to_tensor_jax_dtype(val: TfVal,
                               jax_dtype: DType | None = None,
                               memoize_constants=False) -> tuple[TfVal, DType]:
  """Converts a scalar, ndarray, or tf.Tensor to a tf.Tensor with proper type.

  If `jax_dtype` is missing, uses JAX typing rules.
  See README.md for details regarding 64-bit values.

  Args:
    val: a scalar, ndarray, tf.Tensor, or tf.Variable
    jax_dtype: an optional dtype to use. If missing, uses JAX type inference
      rules for constants.
    memoize_constants: whether to memoize TF constants. We can't do this
      everywhere, we may be outside of a conversion scope.

  Returns:
    a tuple with a tf.Tensor with the type as needed by JAX, and the JAX type.
  """
  if isinstance(val, (tf.Tensor, tf.Variable)):
    jax_dtype = jax_dtype or _to_jax_dtype(val.dtype)  # Give JAX a chance to pick the type
    conversion_dtype = _to_tf_dtype(jax_dtype)
    if conversion_dtype != val.dtype:  # May need to cast for 64-bit values
      return tf.cast(val, conversion_dtype), jax_dtype
    else:
      return val, jax_dtype
  else:  # A constant
    jax_dtype = jax_dtype or core.typeof(val).dtype
    # TODO(document): We assume that the value of a constant does not
    # change through the scope of the function. But it may be an ndarray, ...
    # JAX has the same problem when generating HLO.
    const_key = (id(val), jax_dtype)
    # Since we use id(val) as a cache key, we have to make sure that we keep
    # the previous `val` alive. Otherwise, for a ndarray, it can get garbage
    # collected and reused for a different value, which would create correctness
    # issues. We keep the `val` alive by storing in the cache the pair
    # `(val, tf_val)`.
    # Only memoize non-scalars. JAX will lift all non-scalar constants as
    # Jaxpr consts, to the top level of the Jaxpr. This ensures that we see them
    # early, when entering the Jaxpr, so we create the tf.const early and its
    # scope is the entire Jaxpr.
    do_memoize = (memoize_constants and np.size(val) > 1 and _thread_local_state.constant_cache is not None)
    if do_memoize:
      _, tf_val = _thread_local_state.constant_cache.get(const_key, (None, None))
    else:
      tf_val = None
    if tf_val is None:
      conversion_dtype = _to_tf_dtype(jax_dtype)
      # The float0 type is not known to TF.
      if jax_dtype == dtypes.float0:
        val = np.zeros(np.shape(val), conversion_dtype.as_numpy_dtype)
      if hasattr(val, 'dtype') and dtypes.issubdtype(val.dtype, dtypes.extended):
        val = val.dtype._rules.physical_const(val)
      tf_val = tf.convert_to_tensor(val, dtype=conversion_dtype)
      if do_memoize:
        _thread_local_state.constant_cache[const_key] = (val, tf_val)
    return tf_val, jax_dtype

