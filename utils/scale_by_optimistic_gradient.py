
def scale_by_optimistic_gradient(
    alpha: jax.typing.ArrayLike = 1.0, beta: jax.typing.ArrayLike = 1.0
) -> base.GradientTransformation:
  """Compute generalized optimistic gradients.

  See :func:`optax.optimistic_adam_v2`,
  :func:`optax.optimistic_gradient_descent` for more details.

  Args:
    alpha: Coefficient for generalized optimistic gradient descent.
    beta: Coefficient for negative momentum.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def init_fn(params):
    return ScaleByOptimisticGradientState(
        is_initial_step=jnp.array(True),
        previous_gradient=optax.tree.zeros_like(params),
    )

  def update_fn(updates, state, params=None):
    del params

    def f(grad, prev_grad):
      # At the initial step, the previous gradient doesn't exist, so we use the
      # current gradient instead.
      # https://github.com/google-deepmind/optax/issues/1082
      prev_grad = jnp.where(state.is_initial_step, grad, prev_grad)
      return (alpha + beta) * grad - beta * prev_grad

    new_updates = jax.tree.map(f, updates, state.previous_gradient)

    new_state = ScaleByOptimisticGradientState(
        is_initial_step=jnp.array(False),
        previous_gradient=updates,
    )

    return new_updates, new_state

  return base.GradientTransformation(init_fn, update_fn)

