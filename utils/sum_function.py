
def sum_function(nonbatch_arg, batch_arg1, batch_arg2):
  return jnp.sum(nonbatch_arg + batch_arg1 + 2 * batch_arg2, axis=0)

