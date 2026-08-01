
def _W4(N: int, k: Array) -> Array:
  N_arr, k = promote_dtypes_complex(N, k)
  return jnp.exp(-.5j * np.pi * k / N_arr)

