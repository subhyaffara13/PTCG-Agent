
def wrap_key_data(key_bits_array: Array, *,
                  impl: PRNGSpecDesc | None = None,
                  dtype: KeyDTypeLike | None = None):
  """Wrap an array of key data bits into a PRNG key array.

  Args:
    key_bits_array: a ``uint32`` array with trailing shape corresponding to
      the key shape of the PRNG implementation specified by ``impl``.
    impl: optional, specifies a PRNG implementation, as in ``random.key``.
    dtype: optional dtype or string name specifying the PRNG implementation
      (e.g. ``jax.random.key_dtype('threefry2x32')`` or ``'threefry2x32'``).

  Returns:
    A PRNG key array, whose dtype is a subdtype of ``jax.dtypes.prng_key``
      corresponding to ``impl``, and whose shape equals the leading shape
      of ``key_bits_array.shape`` up to the key bit dimensions.

  Examples:
    Construct a key, and extract its data and dtype:

    >>> import jax
    >>> key = jax.random.key(42)
    >>> data = jax.random.key_data(key)
    >>> dtype = key.dtype

    Reconstruct an equivalent key with :func:`wrap_key_data`:

    >>> new_key = jax.random.wrap_key_data(data, dtype=dtype)
    >>> key == new_key
    Array(True, dtype=bool)
  """
  if dtype is not None:
    if impl is not None:
      raise ValueError(
          "Cannot specify both `impl` and `dtype` arguments to"
          " jax.random.wrap_key_data")
    impl = dtype
  impl_obj = resolve_prng_impl(impl)
  return prng.random_wrap(key_bits_array, impl=impl_obj)

