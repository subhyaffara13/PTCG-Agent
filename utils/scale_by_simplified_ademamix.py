
def scale_by_simplified_ademamix(
    b1: jax.typing.ArrayLike = 0.99,
    b2: jax.typing.ArrayLike = 0.95,
    alpha: base.ScalarOrSchedule = 0.0,
    eps: jax.typing.ArrayLike = 1e-8,
    eps_root: jax.typing.ArrayLike = 0.0,
) -> base.GradientTransformation:
  """Scale updates according to the Simplified AdEMAMix optimizer.

  See :func:`optax.contrib.simplified_ademamix.` for a full description.

  References:
    Morwani et al, `Connections between Schedule-Free Optimizers, AdEMAMix, and
    Accelerated SGD Variants <https://arxiv.org/abs/2502.02431>`_, 2025

  Args:
    b1: Exponential decay rate to track the EMA.
    b2: Exponential decay rate to track the second moment of past gradients.
    alpha: Mixing coefficient for the current gradient and EMA.
    eps: A small constant applied to denominator outside of the square root (as
      in the Adam paper) to avoid dividing by zero when rescaling.
    eps_root: A small constant applied to denominator inside the square root (as
      in RMSProp), to avoid dividing by zero when rescaling. This is needed for
      instance when computing (meta-)gradients through Adam.

  Returns:
    The corresponding `GradientTransformation`.
  """

  def init_fn(params) -> ScaleBySimplifiedAdEMAMixState:
    return ScaleBySimplifiedAdEMAMixState(
        t=jnp.array(0, jnp.int32),
        m=optax.tree.zeros_like(params),
        n=optax.tree.zeros_like(params),
    )

  def update_fn(updates, state, params=None):
    del params
    c_alpha = alpha(state.t) if callable(alpha) else alpha

    g = updates
    m = optax.tree.add_scale(g, b1, state.m)
    n = lerp(b2, optax.tree.mul(g, g), state.n)

    t = numerics.safe_increment(state.t)

    n_hat = optax.tree.bias_correction(n, b2, t)

    u_num = optax.tree.add_scale(m, c_alpha, g)
    u_den = jax.tree.map(lambda n: jnp.sqrt(n + eps_root) + eps, n_hat)

    u = optax.tree.div(u_num, u_den)

    return u, ScaleBySimplifiedAdEMAMixState(t=t, m=m, n=n)

  return base.GradientTransformation(init_fn, update_fn)

