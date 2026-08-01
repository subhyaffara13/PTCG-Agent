
def cast_to_e8m0_with_rounding_up(x):
  temp = x.astype(np.float32).view(np.uint32)
  exp = temp >> 23
  mant = temp & 0x7FFFFF
  is_ru = jnp.logical_and(
      jnp.logical_and((mant > 0), (exp != 0xFE)),
      ~jnp.logical_and((exp == 0), (mant <= 0x400000))
  )
  exp = jnp.where(is_ru, exp + 1, exp)
  new_x = exp.astype(np.uint8)
  return new_x

