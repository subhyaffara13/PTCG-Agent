
def _scale_broadcast(
    scale: Array,
    operand_shape: tuple[int, ...],
    contracting_dims: Sequence[int],
) -> Array:
  for i in contracting_dims:
    if scale.shape[i] != operand_shape[i]:
      multiplier = operand_shape[i] // scale.shape[i]
      new_broadcast_shape = list(scale.shape)
      new_broadcast_shape.insert(i + 1, multiplier)
      scale = jnp.expand_dims(scale, axis=i + 1)
      scale = jnp.broadcast_to(scale, new_broadcast_shape)
      new_reshape_shape = list(scale.shape)
      new_reshape_shape[i] = new_reshape_shape[i] * new_reshape_shape[i + 1]
      new_reshape_shape.pop(i + 1)
      scale = scale.reshape(new_reshape_shape)
  return scale

