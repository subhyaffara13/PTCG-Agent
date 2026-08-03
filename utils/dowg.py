from typing import Any, Callable, Optional, Union

def dowg(
    learning_rate: base.ScalarOrSchedule = 1.0,
    init_estim_sq_dist: Optional[jax.typing.ArrayLike] = None,
    eps: jax.typing.ArrayLike = 1e-4,
    weight_decay: Optional[jax.typing.ArrayLike] = None,
    mask: Optional[Union[Any, Callable[[base.Params], Any]]] = None,
):
  r"""Distance over weighted Gradients optimizer.

  Examples:
    >>> import optax
    >>> from optax import contrib
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = contrib.dowg()
    >>> params = jnp.array([1., 2., 3.])
    >>> print('Objective function: ', f(params))
    Objective function:  14.0
    >>> opt_state = solver.init(params)
    >>> for _ in range(5):
    ...  value, grad = jax.value_and_grad(f)(params)
    ...  updates, opt_state = solver.update(
    ...    grad, opt_state, params, value=value)
    ...  params = optax.apply_updates(params, updates)
    ...  print('Objective function: ', f(params))
    Objective function:  13.925367
    Objective function:  13.872763
    Objective function:  13.775433
    Objective function:  13.596172
    Objective function:  13.268837

  References:
    Khaled et al., `DoWG Unleashed: An Efficient Universal Parameter-Free
    Gradient Descent Method <https://arxiv.org/pdf/2305.16284>`_, 2023.

  Args:
    learning_rate: optional learning rate (potentially varying according to some
      predetermined scheduler).
    init_estim_sq_dist: initial guess of the squared distance to solution.
    eps: small value to prevent division by zero in the denominator defining,
      the learning rate, also used as initial guess for the distance to solution
      if ``init_estim_sq_dist`` is None.
    weight_decay: Strength of the weight decay regularization.
    mask: A tree with same structure as (or a prefix of) the params PyTree, or a
      Callable that returns such a pytree given the params/updates. The leaves
      should be booleans, `True` for leaves/subtrees you want to apply the
      weight decay to, and `False` for those you want to skip. Note that the
      gradient transformations is applied to all parameters.

  Returns:
    The corresponding :class:`optax.GradientTransformation`.

  .. versionadded:: 0.2.3
  """
  return combine.chain(
      transform.add_decayed_weights(weight_decay, mask)
      if weight_decay is not None
      else base.identity(),
      scale_by_dowg(init_estim_sq_dist, eps),
      transform.scale_by_learning_rate(learning_rate),
  )

