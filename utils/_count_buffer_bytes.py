import math


def _count_buffer_bytes(shape_dtype: jax.ShapeDtypeStruct) -> int:
  return math.prod(shape_dtype.shape) * dtypes.itemsize_bits(dtypes.dtype(shape_dtype.dtype)) // 8

