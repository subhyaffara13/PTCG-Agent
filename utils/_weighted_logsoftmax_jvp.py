
def _weighted_logsoftmax_jvp(primals, tangents):
  """Custom JVP of weighted logsoftmax."""
  (x, weights) = primals
  (x_dot, weights_dot) = tangents
  logsoftmax_x = jax.nn.log_softmax(x, axis=-1)
  result = jnp.where(
      weights != 0.0, weights * logsoftmax_x, jnp.zeros_like(logsoftmax_x)
  )
  out_tangents = (
      weights * x_dot
      - weights
      * jnp.sum(x_dot * jax.nn.softmax(x, axis=-1), axis=-1, keepdims=True)
      + weights_dot * logsoftmax_x
  )
  return result, out_tangents

