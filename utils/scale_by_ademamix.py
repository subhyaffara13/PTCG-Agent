
def scale_by_ademamix(
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.999,
    b3: base.ScalarOrSchedule = 0.9999,
    alpha: base.ScalarOrSchedule = 6.0,
    eps: jax.typing.ArrayLike = 1e-8,
    eps_root: jax.typing.ArrayLike = 0.0,
    mu_dtype: Optional[jax.typing.DTypeLike] = None,
) -> base.GradientTransformation:
  """Scale updates according to the Ademamix algorithm.

  See :func:`optax.contrib.ademamix.` for a full description of the algorithm.

  References:
    Pagliardini et al, `The AdEMAMix Optimizer: Better, Faster, Older
    <https://arxiv.org/abs/2409.03137>`_, 2024

  Args:
    b1: Exponential decay rate to track the fast EMA.
    b2: Exponential decay rate to track the second moment of past gradients.
    b3: Exponential decay rate to track the slow EMA.
    alpha: Mixing coefficient in the linear combination for the fast and slow
      EMAs.
    eps: A small constant applied to denominator outside of the square root (as
      in the Adam paper) to avoid dividing by zero when rescaling.
    eps_root: A small constant applied to denominator inside the square root (as
      in RMSProp), to avoid dividing by zero when rescaling. This is needed for
      instance when computing (meta-)gradients through Adam.
    mu_dtype: Optional `dtype` to be used for the first order accumulator; if
      `None` then the `dtype` is inferred from `params` and `updates`.

  Returns:
    The corresponding `GradientTransformation`.
  """

  mu_dtype = utils.canonicalize_dtype(mu_dtype)

  def init_fn(params) -> ScaleByAdemamixState:
    m1 = optax.tree.zeros_like(params, dtype=mu_dtype)  # fast EMA
    m2 = optax.tree.zeros_like(params, dtype=mu_dtype)  # slow EMA
    nu = optax.tree.zeros_like(params, dtype=mu_dtype)  # second moment estimate
    return ScaleByAdemamixState(
        count=jnp.zeros([], jnp.int32),
        count_m2=jnp.zeros([], jnp.int32),
        m1=m1,
        m2=m2,
        nu=nu,
    )

  def update_fn(updates, state, params=None):
    del params
    c_b3 = b3(state.count_m2) if callable(b3) else b3
    c_alpha = alpha(state.count_m2) if callable(alpha) else alpha
    m1 = optax.tree.update_moment(
        updates, state.m1, b1, order=1
    )  # m1 = b1 * m1 + (1-b1) * updates
    m2 = optax.tree.update_moment(updates, state.m2, c_b3, order=1)
    nu = optax.tree.update_moment_per_elem_norm(updates, state.nu, b2, order=2)
    count_inc = numerics.safe_int32_increment(state.count)
    count_m2_inc = numerics.safe_int32_increment(state.count_m2)
    m1_hat = optax.tree.bias_correction(m1, b1, count_inc)
    # NOTE:  AdEMAMix does not perform bias correction on b2 to let
    # the slow EMA momentum buffer fill itself slowly.
    nu_hat = optax.tree.bias_correction(nu, b2, count_inc)
    updates = jax.tree.map(
        lambda m1_, m2_, v_: (
            (m1_ + c_alpha * m2_) / (jnp.sqrt(v_ + eps_root) + eps)
        ),
        m1_hat,
        m2,
        nu_hat,
    )
    return updates, ScaleByAdemamixState(
        count=count_inc, count_m2=count_m2_inc, m1=m1, m2=m2, nu=nu
    )

  return base.GradientTransformation(init_fn, update_fn)

