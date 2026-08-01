
def e8m0_to_dtype(x, dtype):
  temp = x.astype(np.uint32)
  exp = temp << 23
  new_x = exp.view(np.float32)
  near_zero_value = 2**-15 if dtype == np.float16 else 2**-127
  new_x = jnp.where(
      new_x == 0, jnp.array(near_zero_value, np.float32), new_x
  )
  return new_x.astype(dtype)

