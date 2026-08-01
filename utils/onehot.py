
def onehot(labels, num_classes, on_value=1.0, off_value=0.0):
  """Create a dense one-hot version of an indexed array.

  NB: consider using the more standard ``jax.nn.one_hot`` instead.

  Args:
    labels: an n-dim JAX array whose last dimension contains integer indices.
    num_classes: the maximum possible index.
    on_value: the "on" value for the one-hot array, defaults to 1.0.
    off_value: the "off" value for the one-hot array, defaults to 0.0.
  Returns:
    A (n+1)-dim array whose last dimension contains one-hot vectors of length
    num_classes.
  """
  x = labels[..., None] == jnp.arange(num_classes).reshape(
    (1,) * labels.ndim + (-1,)
  )
  x = lax.select(x, jnp.full(x.shape, on_value), jnp.full(x.shape, off_value))
  return x.astype(jnp.float32)

