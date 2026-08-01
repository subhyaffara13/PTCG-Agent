
def sum_function_with_kwargs(nonbatch_arg, batch_arg1, *, batch_kwarg2):
  return jnp.sum(nonbatch_arg + batch_arg1 + 2 * batch_kwarg2, axis=0)

