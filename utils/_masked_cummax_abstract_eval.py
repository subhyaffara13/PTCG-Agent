
def _masked_cummax_abstract_eval(x, mask):
  if x.dtype not in (jnp.uint32, jnp.int32, jnp.float32):
    raise NotImplementedError(
        f"x.dtype={x.dtype} must be uint32, int32 or float32")
  if not jnp.issubdtype(mask.dtype, jnp.bool):
    raise TypeError(f"mask.dtype={mask.dtype} is not a boolean dtype")
  if x.shape != mask.shape:
    raise ValueError(f"x.shape={x.shape} != mask.shape={mask.shape}")
  return x

