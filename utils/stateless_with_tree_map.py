from typing import Callable, Optional

def stateless_with_tree_map(
    f: Callable[[jax.typing.ArrayLike, Optional[jax.typing.ArrayLike]],
                jax.typing.ArrayLike],
) -> GradientTransformation:
  """Creates a stateless transformation from an update-like function for arrays.

  This wrapper eliminates the boilerplate needed to create a transformation that
  does not require saved state between iterations, just like optax.stateless.
  In addition, this function will apply the tree map over update/params for you.

  Args:
    f: Update function that takes in an update array (e.g. gradients) and
      parameter array and returns an update array. The parameter array may be
      `None`.

  Returns:
    A :class:`optax.GradientTransformation`.
  """

  def update_fn(updates, state, params=None):
    del state
    if params is not None:
      return jax.tree.map(f, updates, params), EmptyState()
    else:
      f_ = lambda u: f(u, None)
      return jax.tree.map(f_, updates), EmptyState()

  return GradientTransformation(init_empty_state, update_fn)

