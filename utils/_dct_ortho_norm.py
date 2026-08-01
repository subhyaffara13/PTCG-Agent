
def _dct_ortho_norm(out: Array, axis: int) -> Array:
  factor = lax.concatenate([lax.full((1,), 4, out.dtype), lax.full((out.shape[axis] - 1,), 2, out.dtype)], 0)
  factor = lax.expand_dims(factor, [a for a in range(out.ndim) if a != axis])
  return out / lax.sqrt(factor * out.shape[axis])

