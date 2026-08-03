from typing import Optional

def scale_by_lion(
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.99,
    mu_dtype: Optional[jax.typing.DTypeLike] = None,
    *,
    mode: Literal['hard', 'smooth', 'refined'] = 'hard',
    smooth_beta: float = 1.0,
) -> base.GradientTransformation:
  """Rescale updates according to the Lion algorithm.

  See :func:`optax.lion` for more details.

  Args:
    b1: Rate for combining the momentum and the current grad.
    b2: Decay rate for the exponentially weighted average of grads.
    mu_dtype: Optional `dtype` to be used for the momentum; if `None` then the
      `dtype is inferred from `params` and `updates`.
    mode : Which sign variant to use: "Hard (sign)", "smooth (tanh smoothing),"
      or "refined" (linear around 0, saturate to sign for a large value).
    smooth_beta: Smoothing factor used when mode == "smooth"

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  mu_dtype = utils.canonicalize_dtype(mu_dtype)

  def init_fn(params):
    mu = optax.tree.zeros_like(params, dtype=mu_dtype)  # moment
    return ScaleByLionState(count=jnp.zeros([], jnp.int32), mu=mu)

  def update_fn(updates, state, params=None):

    del params

    def _comb(g, m):
      x = (1.0 - b1) * g + b1 * m
      if mode == 'hard':
        return jnp.sign(x)
      elif mode == 'smooth':
        return jnp.tanh(smooth_beta * x)
      elif mode == 'refined':
        # Keep small values linear, saturate to sign for large values.
        return jnp.where(jnp.abs(x) < 1.0, x, jnp.sign(x))
      else:  # pytype: disable=unreachable
        raise ValueError(
            f'Unknown lion mode: {mode}. '
            'It needs to be one of ["hard", "smooth", "refined"].'
        )

    updates_new = jax.tree.map(_comb, updates, state.mu)
    mu = optax.tree.update_moment(updates, state.mu, b2, 1)
    mu = optax.tree.cast(mu, mu_dtype)
    count_inc = numerics.safe_increment(state.count)
    return updates_new, ScaleByLionState(count=count_inc, mu=mu)

  return base.GradientTransformation(init_fn, update_fn)

