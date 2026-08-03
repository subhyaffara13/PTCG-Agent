import random

def _complex_uniform(key: Array,
                     shape: Sequence[int],
                     dtype: DType) -> Array:
  """
  Sample uniform random values within a disk on the complex plane,
  with zero mean and unit variance.
  """
  key_r, key_theta = random.split(key)
  real_dtype = np.array(0, dtype).real.dtype
  dtype = dtypes.to_complex_dtype(real_dtype)
  r = jnp.sqrt(2 * random.uniform(key_r, shape, real_dtype)).astype(dtype)
  theta = 2 * np.pi * random.uniform(key_theta, shape, real_dtype).astype(dtype)
  return r * jnp.exp(1j * theta)

