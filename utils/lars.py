
def lars(
    learning_rate: base.ScalarOrSchedule,
    weight_decay: base.ScalarOrSchedule = 0.0,
    weight_decay_mask: MaskOrFn = True,
    trust_coefficient: jax.typing.ArrayLike = 0.001,
    eps: jax.typing.ArrayLike = 0.0,
    trust_ratio_mask: MaskOrFn = True,
    momentum: jax.typing.ArrayLike = 0.9,
    nesterov: bool = False,
) -> base.GradientTransformationExtraArgs:
  """The LARS optimizer.

  LARS is a layer-wise adaptive optimizer introduced to help scale SGD to
  larger batch sizes. LARS later inspired the LAMB optimizer.

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    weight_decay: Strength of the weight decay regularization.
    weight_decay_mask: A tree with same structure as (or a prefix of) the params
      PyTree, or a Callable that returns such a pytree given the params/updates.
      The leaves should be booleans, `True` for leaves/subtrees you want to
      apply the transformation to, and `False` for those you want to skip.
    trust_coefficient: A multiplier for the trust ratio.
    eps: Optional additive constant in the trust ratio denominator.
    trust_ratio_mask: A tree with same structure as (or a prefix of) the params
      PyTree, or a Callable that returns such a pytree given the params/updates.
      The leaves should be booleans, `True` for leaves/subtrees you want to
      apply the transformation to, and `False` for those you want to skip.
    momentum: Decay rate for momentum.
    nesterov: Whether to use Nesterov momentum.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.lars(learning_rate=0.003)
    >>> params = jnp.array([1., 2., 3.])
    >>> print('Objective function: ', f(params))
    Objective function:  14.0
    >>> opt_state = solver.init(params)
    >>> for _ in range(5):
    ...  grad = jax.grad(f)(params)
    ...  updates, opt_state = solver.update(grad, opt_state, params)
    ...  params = optax.apply_updates(params, updates)
    ...  print('Objective function: {:.2E}'.format(f(params)))
    Objective function: 1.40E+01
    Objective function: 1.40E+01
    Objective function: 1.40E+01
    Objective function: 1.40E+01
    Objective function: 1.40E+01

  References:
    You et al, `Large Batch Training of Convolutional Networks
    <https://arxiv.org/abs/1708.03888>`_, 2017
  """
  return combine.chain(
      transform.add_decayed_weights(weight_decay, mask=weight_decay_mask),
      wrappers.masked(
          inner=transform.scale_by_trust_ratio(
              trust_coefficient=trust_coefficient, eps=eps
          ),
          mask=trust_ratio_mask,
      ),
      transform.scale_by_learning_rate(learning_rate),
      transform.trace(decay=momentum, nesterov=nesterov),
  )

