
def centralize() -> base.GradientTransformation:
  """Centralizes gradients by subtracting their mean along leading dimension.

  Returns:
    A :class:`optax.GradientTransformation` object.

  Example:
    >>> import jax.numpy as jnp
    >>> import optax
    >>> grad = jnp.array([[1, 2, 3], [4, 5, 6]])
    >>> opt = optax.centralize()
    >>> state = opt.init(grad)
    >>> updates, state = opt.update(grad, state)
    >>> print(updates)
    [[-1.  0.  1.]
     [-1.  0.  1.]]
    >>> print(state)
    EmptyState()

  References:
    Yong et al, `Gradient Centralization: A New Optimization Technique for Deep
    Neural Networks <https://arxiv.org/abs/2004.01461>`_, 2020.
  """

  def update_fn(updates, state, params=None):
    del params
    updates = jax.tree.map(_subtract_mean, updates)
    return updates, state

  return base.GradientTransformation(base.init_empty_state, update_fn)

