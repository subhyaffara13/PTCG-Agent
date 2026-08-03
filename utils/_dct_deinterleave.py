import math


def _dct_deinterleave(x: Array, axis: int) -> Array:
  empty_slice = slice(None, None, None)
  ix0 = tuple(
      slice(None, math.ceil(x.shape[axis]/2), 1) if i == axis else empty_slice
      for i in range(len(x.shape)))
  ix1  = tuple(
      slice(math.ceil(x.shape[axis]/2), None, 1) if i == axis else empty_slice
      for i in range(len(x.shape)))
  v0 = x[ix0]
  v1 = lax.rev(x[ix1], (axis,))
  out = jnp.zeros(x.shape, dtype=x.dtype)
  evens = tuple(
      slice(None, None, 2) if i == axis else empty_slice for i in range(len(x.shape)))
  odds = tuple(
      slice(1, None, 2) if i == axis else empty_slice for i in range(len(x.shape)))
  out =  out.at[evens].set(v0)
  out = out.at[odds].set(v1)
  return out

