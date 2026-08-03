from typing import Optional

def scale_by_polyak(
    f_min: jax.typing.ArrayLike = 0.0,
    max_learning_rate: jax.typing.ArrayLike = 1.0,
    eps: jax.typing.ArrayLike = 0.0,
    variant: str = 'sps',
) -> base.GradientTransformationExtraArgs:
  r"""Scales the update by Polyak's step-size.

  See :func:`optax.polyak_sgd` for more details.

  Args:
    f_min: a lower bound on the objective function (defaults to 0). Corresponds
      to :math:`f^\star` in the formula above.
    max_learning_rate: a maximum step size to use (defaults to 1).
    eps: a value to add in the denominator of the update (defaults to 0).
    variant: either ``'sps'`` or ``'sps+'`` (defaults to ``'sps'``).

  Returns:
    A :class:`optax.GradientTransformationExtraArgs`, where the ``update``
    function takes an additional keyword argument ``value`` containing the
    current value of the objective function.
  """

  def update_fn(
      updates: base.Updates,
      state: base.EmptyState,
      params: Optional[base.Params] = None,
      *,
      value: jax.typing.ArrayLike,
      **extra_args,
  ) -> tuple[base.Updates, base.EmptyState]:
    """Scales the update by the Polyak step-size.

    Args:
      updates: the updates to be scaled.
      state: the state of the transformation.
      params: the parameters of the model.
      value: the value of the loss function.
      **extra_args: unused,complying with GradientTransformationExtraArgs.

    Returns:
      The scaled updates and the state of the transformation.
    """
    del params
    # complies with signature of GradientTransformationExtraArgs but ignores the
    # extra_args
    del extra_args
    grad_sq_norm = optax.tree.norm(updates, squared=True)
    gap = jnp.array(value - f_min).astype(grad_sq_norm.dtype)
    if variant == 'sps':
      pass
    elif variant == 'sps+':
      gap = nn.relu(gap)
    else:
      raise ValueError(f'Invalid argument value for Polyak SGD: {variant=}')
    # avoid division by zero
    step = jnp.where(
        grad_sq_norm + eps <= jnp.finfo(float).eps,
        jnp.array(0.0),
        jnp.minimum(gap / (grad_sq_norm + eps), max_learning_rate),
    )
    updates = optax.tree.scale(step, updates)
    return updates, state

  return base.GradientTransformationExtraArgs(base.init_empty_state, update_fn)

