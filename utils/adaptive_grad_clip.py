from typing import Optional, Union

def adaptive_grad_clip(
    clipping: jax.typing.ArrayLike,  # float
    eps: jax.typing.ArrayLike = 1e-3,
    axis: Optional[Union[int, tuple[int, ...]]] = None,
) -> base.GradientTransformation:
  """Clips updates to be at most ``clipping * parameter_norm``, unit-wise.

  Args:
    clipping: The maximum allowed ratio of update norm to parameter norm.
    eps: An epsilon term to prevent clipping of zero-initialized params.
    axis: Axis or axes along which to compute the unit-wise norm. If None, uses
      default behavior based on input dimensions (including Conv3D, ndim=5).
      Provide axis for custom parameter shapes beyond the defaults.

  Returns:
    A :class:`optax.GradientTransformation` object.

  References:
    Brock et al., `High-Performance Large-Scale Image Recognition Without
    Normalization <https://arxiv.org/abs/2102.06171>`_, 2021
  """

  def update_fn(updates, state, params):
    if params is None:
      raise ValueError(base.NO_PARAMS_MSG)
    g_norm, p_norm = jax.tree.map(
        lambda x: unitwise_norm(x, axis=axis), (updates, params)
    )
    # Maximum allowable norm.
    max_norm = jax.tree.map(lambda x: clipping * jnp.maximum(x, eps), p_norm)
    # If grad norm > clipping * param_norm, rescale.
    updates = jax.tree.map(unitwise_clip, g_norm, max_norm, updates)
    return updates, state

  return base.GradientTransformation(base.init_empty_state, update_fn)

