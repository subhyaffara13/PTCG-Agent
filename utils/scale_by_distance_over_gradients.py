
def scale_by_distance_over_gradients(
    reps_rel=1e-6, eps=1e-8, param_dtype=jnp.float32, global_scale=1.0
) -> base.GradientTransformation:
  """Distance-over-gradients learning rate-free optimizer.

  This implementation stores a single copy of the model parameters, plus two
  scalars per parameter array. It is equivalent to "Layer-wise DoG" (LDoG)
  in the paper.

  The authors recommend using model averaging with this optimizer.

  Args:
    reps_rel: Used to compute initial learning rate. Recommended values are 1e-4
      for models using batch norm, 1e-6 otherwise.
    eps: Small loading term to avoid divide-by-zero errors.
    param_dtype: dtype for storing initial parameters.
    global_scale: Global scale factor, typically 1.0 or -1.0

  Returns:
    A :class:`optax.GradientTransformation` object.

  References:
    Ivgi et al, `DoG is SGD's Best Friend: A Parameter-Free Dynamic Step Size
    Schedule <https://arxiv.org/pdf/2302.12022.pdf>`_, 2023
  """

  def _l2(x, y=0.0):
    return jnp.sqrt(jnp.square(x - y).sum())

  def init_fn(params):
    return ScaleByDistanceOverGradientsState(
        # Initial distance (needed to prevent zero step sizes).
        jax.tree.map(lambda x: reps_rel * (1 + _l2(x)), params),
        # Initial gradient sum-of-squares.
        jax.tree.map(lambda x: jnp.zeros(1), params),
        # Initial params, cast to preferred precision.
        optax.tree.cast(params, param_dtype),
    )

  def update_fn(updates, state: ScaleByDistanceOverGradientsState, params):
    # update max distance
    max_dist = jax.tree.map(
        lambda d, x, y: jnp.maximum(d, _l2(x, y)),
        state.max_dist,
        params,
        state.init_params,
    )

    # update gradient sum-of-squares
    g_sos = jax.tree.map(
        lambda x, y: x + jnp.square(y).sum(), state.grad_sum_of_squares, updates
    )

    def _tx(g, d, g_sos):
      """Apply the transformation."""
      eta = global_scale * (d / jnp.sqrt(g_sos + eps))
      return eta * g

    updates = jax.tree.map(_tx, updates, max_dist, g_sos)

    # new state
    state = ScaleByDistanceOverGradientsState(
        max_dist, g_sos, state.init_params
    )

    return updates, state

  return base.GradientTransformation(init_fn, update_fn)

