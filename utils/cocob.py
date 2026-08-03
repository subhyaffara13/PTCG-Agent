from typing import Any, Callable, Optional, Union

def cocob(
    learning_rate: base.ScalarOrSchedule = 1.0,
    alpha: jax.typing.ArrayLike = 100.0,
    eps: jax.typing.ArrayLike = 1e-8,
    weight_decay: jax.typing.ArrayLike = 0.0,
    mask: Optional[Union[Any, Callable[[base.Params], Any]]] = None,
) -> base.GradientTransformation:
  """Rescale updates according to the COntinuous COin Betting algorithm.

  Algorithm for stochastic subgradient descent. Uses a gambling algorithm to
  find the minimizer of a non-smooth objective function by accessing its
  subgradients. All we need is a good gambling strategy. See Algorithm 2 of:

  Args:
    learning_rate: optional learning rate to e.g. inject some scheduler
    alpha: fraction to bet parameter of the COCOB optimizer
    eps: jitter term to avoid dividing by 0
    weight_decay: L2 penalty
    mask: mask for weight decay

  Returns:
    A `GradientTransformation` object.

  References:
    Orabana et al, `Training Deep Networks without Learning Rates Through Coin
    Betting <https://arxiv.org/pdf/1705.07795.pdf>`_, 2017
  """
  return combine.chain(
      transform.add_decayed_weights(weight_decay, mask),
      transform.scale_by_learning_rate(learning_rate, flip_sign=False),
      scale_by_cocob(alpha, eps),
  )

