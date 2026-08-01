
def _semaphore_read_abstract_eval(
    *avals,
    args_tree,
):
  del avals, args_tree
  return jax_core.ShapedArray((), jnp.dtype("int32"))

