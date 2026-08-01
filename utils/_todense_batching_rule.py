
def _todense_batching_rule(batched_args, batch_dims, *, tree):
  return jax.vmap(partial(_todense_impl, tree=tree), batch_dims)(*batched_args), 0

