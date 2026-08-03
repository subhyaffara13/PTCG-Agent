from typing import Any

def _resize_nearest(x, output_shape: core.Shape):
  input_shape = x.shape
  assert len(input_shape) == len(output_shape)
  spatial_dims = tuple(i for i in range(len(input_shape))
                       if not core.definitely_equal(input_shape[i], output_shape[i]))
  for d in spatial_dims:
    m = input_shape[d]
    n = output_shape[d]
    offsets = (jnp.arange(n, dtype=np.float32) + 0.5) * core.dimension_as_value(m) / core.dimension_as_value(n)
    # TODO(b/206898375): this computation produces the wrong result on
    # CPU and GPU when using float64. Use float32 until the bug is fixed.
    offsets = jnp.floor(offsets.astype(np.float32)).astype(np.int32)
    indices: list[Any] = [slice(None)] * len(input_shape)
    indices[d] = offsets
    x = x[tuple(indices)]
  return x

