
def _mask_all_reduce_abstract_eval(x, *, reduce):
  if x.dtype != jnp.bool:
    raise TypeError(f"Mask all-reduce only supports bool arrays, got {x.dtype}")
  match x.shape:
    case (minor_dim,):
      return jax_core.ShapedArray((minor_dim // reduce,), jnp.int32)
    case _:
      raise ValueError("Mask all-reduce only supports 1D arrays")

