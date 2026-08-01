
def apply_every(k: jax.typing.ArrayLike = 1) -> base.GradientTransformation:
  """Accumulate gradients and apply them every k steps.

  Note that if this transformation is part of a chain, the states of the other
  transformations will still be updated at every step. In particular, using
  `apply_every` with a batch size of N/2 and k=2 is not necessarily equivalent
  to not using `apply_every` with a batch size of N. If this equivalence is
  important for you, consider using the `optax.MultiSteps`.

  Args:
    k: Emit non-zero gradients every k steps, otherwise accumulate them.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def init_fn(params):
    grad_acc = optax.tree.zeros_like(params)
    return ApplyEvery(count=jnp.zeros([], jnp.int32), grad_acc=grad_acc)

  def update_fn(updates, state, params=None):
    del params
    c = state.count % k
    acc = c != 0
    grad_acc = jax.tree.map(lambda g, ga: acc * ga + g, updates, state.grad_acc)
    emit = c == (k - 1)
    updates = jax.tree.map(lambda ga: emit * ga, grad_acc)
    count_inc = numerics.safe_increment(state.count)
    return updates, ApplyEvery(count=count_inc % k, grad_acc=grad_acc)

  return base.GradientTransformation(init_fn, update_fn)

