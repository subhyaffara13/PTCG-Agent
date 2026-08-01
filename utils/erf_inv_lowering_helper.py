
def erf_inv_lowering_helper(x):
  if x.dtype == jnp.float32:
    return _erf_inv_32_lowering_helper(x)
  if x.dtype == jnp.float64:
    return _erf_inv_64_lowering_helper(x)
  raise NotImplementedError(f"erf_inv_lowering_helper not implemented for {x.dtype}")

