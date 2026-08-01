
def stateless(
    f: Callable[[Updates, Optional[Params]], Updates],
) -> GradientTransformation:
  """Creates a stateless transformation from an update-like function.

  This wrapper eliminates the boilerplate needed to create a transformation that
  does not require saved state between iterations.

  Args:
    f: Update function that takes in updates (e.g. gradients) and parameters and
      returns updates. The parameters may be `None`.

  Returns:
    A :class:`optax.GradientTransformation`.
  """

  def update_fn(updates, state, params=None):
    del state
    return f(updates, params), EmptyState()

  return GradientTransformation(init_empty_state, update_fn)

