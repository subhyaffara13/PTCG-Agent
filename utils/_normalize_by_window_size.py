
def _normalize_by_window_size(dims, strides, padding):
  def rescale(outputs, inputs, spec):
    if spec is None:
      non_spatial_axes = 0, inputs.ndim - 1
    else:
      non_spatial_axes = spec.index('N'), spec.index('C')

    spatial_shape = tuple(inputs.shape[i]
                          for i in range(inputs.ndim)
                          if i not in non_spatial_axes)
    one = jnp.ones(spatial_shape, dtype=inputs.dtype)
    window_sizes = lax.reduce_window(one, 0., lax.add, dims, strides, padding)
    for i in sorted(non_spatial_axes):
      window_sizes = jnp.expand_dims(window_sizes, i)

    return outputs / window_sizes
  return rescale

