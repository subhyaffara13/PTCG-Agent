
def madgrad(
    learning_rate: base.ScalarOrSchedule,
    momentum: float = 0.9,
    weight_decay: float = 0.0,
    eps: float = 1e-6,
) -> base.GradientTransformation:
  """The MADGRAD optimizer.

  MADGRAD is a general purpose optimizer that matches the performance of
  SGD+Momentum on vision tasks and Adam on NLP tasks.

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler.
    momentum: Momentum parameter (default: 0.9).
    weight_decay: Strength of the weight decay regularization (L2).
    eps: Term added to the denominator to improve numerical stability.

  Returns:
    The corresponding :class:`optax.GradientTransformation`.

  References:
    Defazio et al, `Adaptivity without Compromise: A Momentumized, Adaptive,
    Dual Averaged Gradient Method for Stochastic Optimization
    <https://arxiv.org/abs/2101.11075>`_, 2021.
  """
  return combine.chain(
      transform.add_decayed_weights(weight_decay),
      scale_by_madgrad(learning_rate=learning_rate, momentum=momentum, eps=eps)
  )

