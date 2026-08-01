
def scale_by_adan(
    b1: jax.typing.ArrayLike = 0.98,
    b2: jax.typing.ArrayLike = 0.92,
    b3: jax.typing.ArrayLike = 0.99,
    eps: jax.typing.ArrayLike = 1e-8,
    eps_root: jax.typing.ArrayLike = 0.0,
) -> base.GradientTransformation:
  """Rescale updates according to the Adan algorithm.

  See :func:`optax.adan` for more details.

  Args:
    b1: Decay rate for the EWMA of gradients.
    b2: Decay rate for the EWMA of differences of gradients.
    b3: Decay rate for the EMWA of the algorithm's squared term.
    eps: Term added to the denominator to improve numerical stability.
    eps_root: Term added to the denominator inside the square-root to improve
      numerical stability when backpropagating gradients through the rescaling.

  Returns:
    An :class:`optax.GradientTransformation` object.
  """

  def init_fn(params):
    return ScaleByAdanState(
        m=optax.tree.zeros_like(params),
        v=optax.tree.zeros_like(params),
        n=optax.tree.zeros_like(params),
        g=optax.tree.zeros_like(params),
        t=jnp.zeros([], jnp.int32),
    )

  def update_fn(updates, state, params=None):
    """Based on Algorithm 1 in https://arxiv.org/pdf/2208.06677v4#page=6."""
    del params
    g = updates

    diff = optax.tree.where(
        state.t == 0,
        optax.tree.zeros_like(g),
        optax.tree.sub(g, state.g),
    )
    m = optax.tree.update_moment(g, state.m, b1, 1)
    v = optax.tree.update_moment(diff, state.v, b2, 1)

    sq = optax.tree.add_scale(g, 1 - b2, diff)
    n = optax.tree.update_moment_per_elem_norm(sq, state.n, b3, 2)

    t = numerics.safe_increment(state.t)
    m_hat = optax.tree.bias_correction(m, b1, t)
    v_hat = optax.tree.bias_correction(v, b2, t)
    n_hat = optax.tree.bias_correction(n, b3, t)

    u = optax.tree.add_scale(m_hat, 1 - b2, v_hat)
    denom = jax.tree.map(lambda n_hat: jnp.sqrt(n_hat + eps_root) + eps, n_hat)
    u = optax.tree.div(u, denom)

    new_state = ScaleByAdanState(
        m=m,
        v=v,
        n=n,
        g=g,
        t=t,
    )

    return u, new_state

  return base.GradientTransformation(init_fn, update_fn)

