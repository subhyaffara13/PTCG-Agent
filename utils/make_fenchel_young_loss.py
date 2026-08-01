
def make_fenchel_young_loss(max_fun: MaxFun):
  """Creates a Fenchel-Young loss from a max function.

  Args:
    max_fun: the max function on which the Fenchel-Young loss is built.

  Returns:
    A Fenchel-Young loss function with the same signature.

  Examples:
    Given a max function, e.g., the log sum exp, you can construct a
    Fenchel-Young loss easily as follows:

    >>> from jax.scipy.special import logsumexp
    >>> fy_loss = optax.losses.make_fenchel_young_loss(max_fun=logsumexp)

  Reference:
    Blondel et al. `Learning with Fenchel-Young Losses
    <https://arxiv.org/pdf/1901.02324.pdf>`_, 2020

  .. warning::
    The resulting loss accepts an arbitrary number of leading dimensions
    with the fy_loss operating over the last dimension. The jaxopt version of
    this function would instead flatten any vector in a single big 1D vector.
  """

  vdot_last_dim = jnp.vectorize(jnp.vdot, signature="(n),(n)->()")
  max_fun_last_dim = jnp.vectorize(max_fun, signature="(n)->()")

  def fenchel_young_loss(scores, targets, *args, **kwargs):
    max_value = max_fun_last_dim(scores, *args, **kwargs)
    return max_value - vdot_last_dim(targets, scores)

  return fenchel_young_loss

