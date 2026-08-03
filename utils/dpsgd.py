from typing import Optional

def dpsgd(
    learning_rate: base.ScalarOrSchedule,
    l2_norm_clip: jax.typing.ArrayLike,
    noise_multiplier: jax.typing.ArrayLike,
    seed: int,
    momentum: Optional[jax.typing.ArrayLike] = None,
    nesterov: bool = False,
) -> base.GradientTransformation:
  """The DPSGD optimizer.

  Differential privacy is a standard for privacy guarantees of algorithms
  learning from aggregate databases including potentially sensitive information.
  DPSGD offers protection against a strong adversary with full knowledge of the
  training mechanism and access to the model's parameters.

  Args:
    learning_rate: A fixed global scaling factor.
    l2_norm_clip: Maximum L2 norm of the per-example gradients.
    noise_multiplier: Ratio of standard deviation to the clipping norm.
    seed: Initial seed used for the jax.random.PRNGKey
    momentum: Decay rate used by the momentum term, when it is set to `None`,
      then momentum is not used at all.
    nesterov: Whether Nesterov momentum is used.

  Returns:
    A :class:`optax.GradientTransformation`.

  References:
    Abadi et al, 2016 `Deep Learning with Differential Privacy
    <https://arxiv.org/abs/1607.00133>`_, 2016

  .. warning::
    This :class:`optax.GradientTransformation` expects input updates to have a
    batch dimension on the 0th axis. That is, this function expects per-example
    gradients as input (which are easy to obtain in JAX using `jax.vmap`).

  .. warning::
    Generic gradient aggregation tools like :class:`optax.MultiSteps` or
    :func:`optax.apply_every` won't work correctly with this transformation
    since the whole point of this transformation is to aggregate gradients in a
    specific way.
  """
  return combine.chain(
      differentially_private_aggregate(
          l2_norm_clip=l2_norm_clip,
          noise_multiplier=noise_multiplier,
          seed=seed,
      ),
      (
          transforms.trace(decay=momentum, nesterov=nesterov)
          if momentum is not None
          else base.identity()
      ),
      transform.scale_by_learning_rate(learning_rate),
  )

