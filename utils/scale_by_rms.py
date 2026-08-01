
def scale_by_rms(
    decay: jax.typing.ArrayLike = 0.9,
    eps: jax.typing.ArrayLike = 1e-8,
    initial_scale: jax.typing.ArrayLike = 0.0,
    eps_in_sqrt: bool = True,
    bias_correction: bool = False,
) -> base.GradientTransformation:
  r"""Rescale updates by the root of the exp. moving avg of the square.

  See :func:`optax.rmsprop` for more details.

  Args:
    decay: Decay rate for the exponentially weighted average of squared grads.
    eps: Term added to the denominator to improve numerical stability.
    initial_scale: Initial value for second moment.
    eps_in_sqrt: Whether to add ``eps`` in the square root of the denominator or
      outside the square root.
    bias_correction: Whether to apply bias correction to the exponentially
      weighted average of squared grads.

  Returns:
    A :class:`optax.GradientTransformation` object.

  .. note::
    Using `scale_by_rms(decay=b2, eps_in_sqrt=False, bias_correction=True)`
    will match the behavior of `scale_by_adam(b1=0, b2=b2)`, while sparing the
    memory cost of storing the first moment.
  """

  def init_fn(params):
    nu = optax.tree.full_like(params, initial_scale)  # second moment
    if bias_correction:
      return ScaleByRmsWithCountState(count=jnp.zeros([], jnp.int32), nu=nu)
    return ScaleByRmsState(nu=nu)

  def update_fn(updates, state, params=None):
    del params
    nu = optax.tree.update_moment_per_elem_norm(updates, state.nu, decay, 2)
    if bias_correction:
      count_inc = numerics.safe_increment(state.count)
      nu_hat = optax.tree.bias_correction(nu, decay, count_inc)
    else:
      count_inc = jnp.asarray(0)
      nu_hat = nu
    if eps_in_sqrt:
      scaling = jax.tree.map(lambda n: jax.lax.rsqrt(n + eps), nu_hat)
    else:
      scaling = jax.tree.map(lambda n: 1 / (jnp.sqrt(n) + eps), nu_hat)
    updates = jax.tree.map(lambda s, g: s * g, scaling, updates)
    if bias_correction:
      new_state = ScaleByRmsWithCountState(count=count_inc, nu=nu)
    else:
      new_state = ScaleByRmsState(nu=nu)
    return updates, new_state

  return base.GradientTransformation(init_fn, update_fn)

