
def get_fp8_max(fp8_dtype, out_dtype):
  assert fp8_dtype in (jnp.float8_e4m3fn, jnp.float8_e5m2,
                       jnp.float8_e4m3fnuz, jnp.float8_e5m2fnuz)
  return jnp.finfo(fp8_dtype).max.astype(out_dtype)

