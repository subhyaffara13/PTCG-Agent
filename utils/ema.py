from typing import Any, Optional

def ema(
    decay: jax.typing.ArrayLike,  # float
    debias: bool = True,
    accumulator_dtype: Optional[Any] = None
) -> base.GradientTransformation:
  """Compute an exponential moving average of past updates.

  Args:
    decay: Decay rate for the exponential moving average.
    debias: Whether to debias the transformed gradient.
    accumulator_dtype: Optional `dtype` to used for the accumulator; if `None`
      then the `dtype` is inferred from `params` and `updates`.

  Returns:
    A :class:`optax.GradientTransformation` object.

  .. note::
    :func:`optax.trace` and :func:`optax.ema` have very similar but distinct
    updates; ``trace = decay * trace + t``, while
    ``ema = decay * ema + (1-decay) * t``.
    Both are frequently found in the optimization literature.
  """

  accumulator_dtype = utils.canonicalize_dtype(accumulator_dtype)

  def init_fn(params):
    return EmaState(
        count=jnp.zeros([], jnp.int32),
        ema=optax.tree.zeros_like(params, dtype=accumulator_dtype),
    )

  def update_fn(updates, state, params=None):
    del params
    updates = new_ema = optax.tree.update_moment(
        updates, state.ema, decay, order=1
    )
    count_inc = numerics.safe_increment(state.count)
    if debias:
      updates = optax.tree.bias_correction(new_ema, decay, count_inc)
    state_ema = optax.tree.cast(new_ema, accumulator_dtype)
    return updates, EmaState(count=count_inc, ema=state_ema)

  return base.GradientTransformation(init_fn, update_fn)

