
def _select_stack_fn(
    items: Sequence[jax.Array],
    sharding: jax.sharding.Sharding | None = None,
) -> Callable[[Sequence[jax.Array | np.ndarray], int], jax.Array | np.ndarray]:
  """Selects the stack function based on the input array sharding.

  * If any of the `items` is a numpy array, use np.stack.
  * If a sharding is specified and all the `items` are jax arrays that live in
    host memory, use _streaming_stack.
  * Otherwise, use jnp.stack.

  Args:
    items: Sequence of arrays to stack.
    sharding: Optional target sharding for the stacked array.

  Returns:
    The stack function to use for the given items.
  """
  if any(isinstance(x, np.ndarray) for x in items):
    return np.stack
  if sharding is not None and all(_is_host_array(x) for x in items):
    return lambda items, axis: _streaming_stack(items, axis, sharding)
  return jnp.stack

