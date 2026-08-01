
def mean_function(nonbatch_arg, batch_arg1, batch_arg2):
  return jnp.mean(nonbatch_arg * batch_arg1), {'key': jnp.mean(batch_arg2)}

