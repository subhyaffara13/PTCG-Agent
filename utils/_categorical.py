
def _categorical(key, logits_arr, shape, batch_shape, axis, replace, mode) -> Array:
  shape_prefix = shape[:len(shape)-len(batch_shape)]
  if replace:
    if axis >= 0:
      axis -= len(logits_arr.shape)

    logits_shape = list(shape[len(shape) - len(batch_shape):])
    logits_shape.insert(axis % len(logits_arr.shape), logits_arr.shape[axis])
    return jnp.argmax(
        gumbel(key, (*shape_prefix, *logits_shape), logits_arr.dtype, mode=mode) +
        lax.expand_dims(logits_arr, tuple(range(len(shape_prefix)))),
        axis=axis)
  else:
    logits_arr += gumbel(key, logits_arr.shape, logits_arr.dtype, mode=mode)
    k = math.prod(shape_prefix)
    if k > logits_arr.shape[axis]:
      raise ValueError(
        f"Number of samples without replacement ({k}) cannot exceed number of "
        f"categories ({logits_arr.shape[axis]})."
      )

    _, indices = lax.top_k(jnp.moveaxis(logits_arr, axis, -1), k)
    assert indices.shape == batch_shape + (k,)
    assert shape == shape_prefix + batch_shape

    dimensions = (indices.ndim - 1, *range(indices.ndim - 1))
    indices = lax.reshape(indices, shape, dimensions)
    assert indices.shape == shape
    return indices

