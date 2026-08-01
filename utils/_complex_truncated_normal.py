
def _complex_truncated_normal(key: Array, upper: ArrayLike,
                              shape: Sequence[int],
                              dtype: DType) -> Array:
  """
  Sample random values from a centered normal distribution on the complex plane,
  whose modulus is truncated to `upper`, and the variance before the truncation
  is one.
  """
  key_r, key_theta = random.split(key)
  real_dtype = np.array(0, dtype).real.dtype
  dtype = dtypes.to_complex_dtype(real_dtype)
  t = ((1 - jnp.exp(jnp.array(-(upper ** 2), dtype)))
       * random.uniform(key_r, shape, real_dtype).astype(dtype))
  r = jnp.sqrt(-jnp.log(1 - t))
  theta = 2 * np.pi * random.uniform(key_theta, shape, real_dtype).astype(dtype)
  return r * jnp.exp(1j * theta)

