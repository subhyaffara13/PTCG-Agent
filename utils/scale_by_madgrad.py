
def scale_by_madgrad(
    learning_rate: base.ScalarOrSchedule,
    momentum: float = 0.9,
    eps: float = 1e-6,
) -> base.GradientTransformation:
  """Rescale updates according to the MADGRAD algorithm.

  MADGRAD is a Dual Averaging method that maintains a weighted sum of gradients
  and squared gradients to compute adaptive updates. It effectively bridges the
  gap between the generalization performance of SGD and the convergence speed
  of adaptive methods like Adam.

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler.
    momentum: Momentum parameter (default: 0.9).
    eps: Term added to the denominator to improve numerical stability.

  Returns:
    A :class:`optax.GradientTransformation` object.

  References:
    Defazio et al, `Adaptivity without Compromise: A Momentumized, Adaptive,
    Dual Averaged Gradient Method for Stochastic Optimization
    <https://arxiv.org/abs/2101.11075>`_, 2021.
  """

  def init_fn(params):
    return MadgradState(
        count=jnp.zeros([], jnp.int32),
        grad_sum_sq=tree.zeros_like(params),
        s=tree.zeros_like(params),
        # Store initial parameters (x0). We use jax.tree.map to handle
        # arbitrary tree structures (including placeholders) correctly.
        x0=jax.tree.map(lambda x: x, params),
    )

  def update_fn(updates, state, params=None):
    if params is None:
      raise ValueError(base.NO_PARAMS_MSG)

    count = state.count
    if callable(learning_rate):
      lr = learning_rate(count)
    else:
      lr = learning_rate

    # Ensure stability by adding eps to the learning rate, matching the
    # official PyTorch implementation.
    lr_stable = lr + eps

    # lamb = lr * sqrt(k + 1)
    lamb = lr_stable * jnp.sqrt(count + 1)

    # G_{k+1} = G_k + lamb * g_k^2
    # We cast the update term to the dtype of g to avoid implicit promotion
    # to float32 (e.g. when g is float16 but lamb is float32).
    grad_sum_sq = jax.tree.map(
        lambda g_sq, g: g_sq + (lamb * (g ** 2)).astype(g.dtype),
        state.grad_sum_sq, updates
    )

    # s_{k+1} = s_k + lamb * g_k
    s = jax.tree.map(
        lambda s_val, g: s_val + (lamb * g).astype(g.dtype),
        state.s, updates
    )

    # sigma_{k+1} = (G_{k+1})^(1/3) + eps
    sigma = jax.tree.map(
        lambda g_sq: jnp.cbrt(g_sq) + eps, grad_sum_sq
    )

    # z_{k+1} = x_0 - s_{k+1} / sigma_{k+1}
    z = jax.tree.map(
        lambda x0_val, s_val, sig: x0_val - s_val / sig, state.x0, s, sigma
    )

    # x_{k+1} = (1 - momentum) * z_{k+1} + momentum * x_k
    x_new = jax.tree.map(
        lambda z_val, x_k: (1 - momentum) * z_val + momentum * x_k,
        z,
        params
    )

    # Convert the new parameter state into an update (x_new - x_old).
    final_updates = jax.tree.map(lambda n, o: n - o, x_new, params)

    new_state = MadgradState(
        count=numerics.safe_increment(count),
        grad_sum_sq=grad_sum_sq,
        s=s,
        x0=state.x0,
    )
    return final_updates, new_state

  return base.GradientTransformation(init_fn, update_fn)

