import functools

def scale_by_sm3(
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 1.0,
    eps: jax.typing.ArrayLike = 1e-8
) -> base.GradientTransformation:
  """Scale updates by `sm3`.

  See :func:`optax.sm3` for more details.

  Args:
    b1: Decay rate for the exponentially weighted average of grads.
    b2: Decay rate for the exponentially weighted average of squared grads.
    eps: Term added to the denominator to improve numerical stability.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def zeros_for_dim(p):
    return [_zeros_like_axis(p, i) for i in range(p.ndim)]

  def init_fn(params):
    _reject_complex(params)
    mu = jax.tree.map(zeros_for_dim, params)
    nu = optax.tree.zeros_like(params)
    return ScaleBySM3State(mu, nu)

  def _expanded_shape(shape, axis):
    # Replaces a `shape` of [M, N, K] with 1 in all dimensions except for i.
    # For eg: i = 1 returns [1, N, 1].
    rank = len(shape)
    return [1] * axis + [shape[axis]] + [1] * (rank - axis - 1)

  def _new_accum(g, v):
    coeffs = ((1.0 - b2) if b2 != 1.0 else 1.0, b2)
    if g.ndim < 2:
      return coeffs[0] * g**2 + coeffs[1] * v[0]
    else:
      return coeffs[0] * g**2 + coeffs[1] * functools.reduce(jnp.minimum, v)

  def _new_mu(g, i):
    if g.ndim < 2:
      return g
    else:
      return jnp.max(g, axis=other_axes(i, g.ndim))

  def other_axes(idx, ndim):
    return list(range(idx)) + list(range(idx + 1, ndim))

  def update_fn(updates, state, params=None):
    del params

    def f(g, v):
      return [
          jnp.reshape(v[i], _expanded_shape(g.shape, i)) for i in range(g.ndim)
      ]

    mu = jax.tree.map(f, updates, state.mu)
    accum = jax.tree.map(_new_accum, updates, mu)
    accum_inv_sqrt = jax.tree.map(
        lambda t: jnp.where(t > 0, jax.lax.rsqrt(t + eps), 0.0), accum
    )
    up = jax.tree.map(lambda g, a: g * a, updates, accum_inv_sqrt)
    nu = optax.tree.update_moment(up, state.nu, b1, 1)
    mu = jax.tree.map(lambda g: [_new_mu(g, i) for i in range(g.ndim)], accum)

    return nu, ScaleBySM3State(mu=mu, nu=nu)

  return base.GradientTransformation(init_fn, update_fn)

