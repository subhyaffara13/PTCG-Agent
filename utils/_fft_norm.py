
def _fft_norm(s: Array, func_name: str, norm: str) -> Array:
  if norm == "backward":
    return jnp.array(1)

  # Avoid potential integer overflow
  s, = promote_dtypes_inexact(s)

  if norm == "ortho":
    return ufuncs.sqrt(reductions.prod(s)) if func_name.startswith('i') else 1/ufuncs.sqrt(reductions.prod(s))
  elif norm == "forward":
    return reductions.prod(s) if func_name.startswith('i') else 1/reductions.prod(s)
  raise ValueError(f'Invalid norm value {norm}; should be "backward",'
                    '"ortho" or "forward".')

