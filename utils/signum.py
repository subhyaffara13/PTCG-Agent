
def signum(a: int) -> int:
    return bool(a > 0) - bool(a < 0)


def signum(
    learning_rate: base.ScalarOrSchedule,
    beta: jax.typing.ArrayLike = 0.9,
    accumulator_dtype: Any | None = None,
) -> base.GradientTransformationExtraArgs:
  r"""A variant of SGD using signs of the components of an EMA of the gradient.

  The update :math:`u_t` is defined from the gradients :math:`g_t` as:

  .. math::
    m_t \leftarrow \beta\, m_t + (1 - \beta)\, g_t \\
    u_t \leftarrow -\alpha_t\, \text{sign}\,(m_t),

  where :math:`\alpha_t` a given learning rate at iteration :math:`t`,
  :math:`m_t` is EMA of the gradient.

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    beta: Exponential moving average decay rate.
    accumulator_dtype: Data type for the EMA accumulator.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  References:
    Bernstein et al., `signSGD: Compressed optimization for Non-Convex Problems
    <https://arxiv.org/abs/1802.04434>`_, 2018

    Zhao et al., 'Deconstructing What Makes a Good Optimizer for Language Models
    <https://arxiv.org/abs/2407.07972>`_, 2024
  """
  return combine.chain(
      # no need to debias the EMA since we're just taking its sign
      transform.ema(beta, debias=False, accumulator_dtype=accumulator_dtype),
      transform.scale_by_sign(),
      transform.scale_by_learning_rate(learning_rate),
  )

