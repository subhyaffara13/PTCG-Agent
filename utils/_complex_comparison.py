from typing import Callable

def _complex_comparison(lax_op: Callable[[ArrayLike, ArrayLike], Array],
                        x: Array, y: Array):
  if dtypes.issubdtype(x.dtype, np.complexfloating):
    return lax.select(lax.eq(x.real, y.real),
                      lax_op(x.imag, y.imag),
                      lax_op(x.real, y.real))
  return lax_op(x, y)

