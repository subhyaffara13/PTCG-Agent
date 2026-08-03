from typing import Callable

def scale_by_factored_rms(
    factored: bool = True,
    decay_rate: jax.typing.ArrayLike = 0.8,
    step_offset: jax.typing.ArrayLike = 0,  # int
    min_dim_size_to_factor: int = 128,
    epsilon: jax.typing.ArrayLike = 1e-30,
    decay_rate_fn: Callable[
        [jax.typing.ArrayLike, jax.typing.ArrayLike],
        jax.typing.ArrayLike] = _decay_rate_pow,  # arg types [int, float]
):
  """Scaling by a factored estimate of the gradient rms (as in Adafactor).

  This is a so-called "1+epsilon" scaling algorithms, that is extremely memory
  efficient compared to RMSProp/Adam, and has had wide success when applied to
  large-scale training of attention-based models.

  Args:
    factored: boolean: whether to use factored second-moment estimates..
    decay_rate: float: controls second-moment exponential decay schedule.
    step_offset: for finetuning, one may set this to the starting step-number of
      the fine tuning phase.
    min_dim_size_to_factor: only factor accumulator if two array dimensions are
      at least this size.
    epsilon: Regularization constant for squared gradient.
    decay_rate_fn: A function that accepts the current step, the decay rate
      parameter and controls the schedule for the second momentum. Defaults to
      the original adafactor's power decay schedule. One potential shortcoming
      of the original schedule is the fact that second momentum converges to 1,
      which effectively freezes the second momentum. To prevent this the user
      can opt for a custom schedule that sets an upper bound for the second
      momentum, like in Zhai et al., 2021.

  Returns:
    The corresponding :class:`optax.GradientTransformation`.

  References:
    Shazeer et al, `Adafactor: Adaptive Learning Rates with Sublinear Memory
    Cost <https://arxiv.org/abs/1804.04235>`_, 2018

    Zhai et al, `Scaling Vision Transformers
    <https://arxiv.org/abs/2106.04560>`_, 2021
  """

  def _to_state(count: jax.typing.ArrayLike, result_tree):
    """Maps from a tree of (factored) values to separate trees of values."""
    return FactoredState(
        count=count,
        v_row=jax.tree.map(lambda o: o.v_row, result_tree),
        v_col=jax.tree.map(lambda o: o.v_col, result_tree),
        v=jax.tree.map(lambda o: o.v, result_tree),
    )

  def init_fn(params):
    """Initialise the optimizer's state."""

    def _init(param):
      shape, dtype = param.shape, param.dtype
      factored_dims = _factored_dims(shape, factored, min_dim_size_to_factor)
      if factored_dims is not None:
        d1, d0 = factored_dims
        return _UpdateResult(
            update=jnp.zeros((1,), dtype=dtype),
            v_row=_zeros_like_no_axis(param, d0),
            v_col=_zeros_like_no_axis(param, d1),
            v=jnp.zeros((1,), dtype=dtype),
        )
      return _UpdateResult(
          update=jnp.zeros((1,), dtype=dtype),
          v_row=jnp.zeros((1,), dtype=dtype),
          v_col=jnp.zeros((1,), dtype=dtype),
          v=jnp.zeros_like(param),
      )

    return _to_state(jnp.zeros([], jnp.int32), jax.tree.map(_init, params))

  def update_fn(grads, state, params):
    """Apply gradient transformation."""
    if params is None:
      raise ValueError(base.NO_PARAMS_MSG)

    def _update(grad, v_row, v_col, v, param, step):
      shape, dtype = param.shape, param.dtype
      decay_rate_t = decay_rate_fn(step - step_offset, decay_rate)

      # Scaled by factorized second moment statistics.
      new_v_row = jnp.zeros((1,), dtype=dtype)
      new_v_col = jnp.zeros((1,), dtype=dtype)
      new_v = jnp.zeros((1,), dtype=dtype)

      factored_dims = _factored_dims(shape, factored, min_dim_size_to_factor)
      if factored_dims is not None:
        d1, d0 = factored_dims
        grad_sqr = numerics.abs_sq(grad) + epsilon
        new_v_row = decay_rate_t * v_row + (1.0 - decay_rate_t) * jnp.mean(
            grad_sqr, axis=d0
        )
        new_v_col = decay_rate_t * v_col + (1.0 - decay_rate_t) * jnp.mean(
            grad_sqr, axis=d1
        )
        new_v_row = new_v_row.astype(dtype)  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
        new_v_col = new_v_col.astype(dtype)  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
        reduced_d1 = d1 - 1 if d1 > d0 else d1
        row_col_mean = jnp.mean(new_v_row, axis=reduced_d1, keepdims=True)
        row_factor = (new_v_row / row_col_mean) ** -0.5
        col_factor = (new_v_col) ** -0.5
        update = (
            grad
            * jnp.expand_dims(row_factor, axis=d0)
            * jnp.expand_dims(col_factor, axis=d1)
        )
      else:
        grad_sqr = numerics.abs_sq(grad) + epsilon
        new_v = decay_rate_t * v + (1.0 - decay_rate_t) * grad_sqr
        new_v = new_v.astype(dtype)  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
        update = grad * (new_v) ** -0.5

      return _UpdateResult(update, new_v_row, new_v_col, new_v)

    # Transform grad and compute new per-parameter stats.
    output = jax.tree.map(
        lambda *args: _update(*args, state.count),
        grads,
        state.v_row,
        state.v_col,
        state.v,
        params,
    )

    # Unpack updates / stats and return.
    updates = jax.tree.map(lambda o: o.update, output)
    return updates, _to_state(numerics.safe_increment(state.count), output)

  return base.GradientTransformation(init_fn, update_fn)

