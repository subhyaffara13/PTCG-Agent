
def _with_extra_batch_axis(
    fun: Function, batch_argnums: Sequence[int]
) -> Function:
  """Wraps a function to add an extra batch axis to the batch_argnums."""
  def wrapped_fun(*args, **kwargs):
    args_with_group_axis = list(args)
    for i in batch_argnums:
      args_with_group_axis[i] = jax.tree.map(
          lambda x: jnp.expand_dims(x, axis=1), args[i]
      )
    return fun(*args_with_group_axis, **kwargs)

  return wrapped_fun

