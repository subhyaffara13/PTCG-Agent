from typing import Callable

def bcast_iotas_to_reshaped_iota(
    add: Callable[[ir.Value, ir.Value], ir.Value],
    mul: Callable[[core.DimSize, ir.Value], ir.Value],
    shape: core.Shape,
    iotas: Sequence[ir.Value]) -> ir.Value:
  strides: core.Shape = (*(np.cumprod(shape[1:][::-1])[::-1]), 1)
  return reduce(add, [mul(s, i) for i, s in zip(iotas, strides)])

