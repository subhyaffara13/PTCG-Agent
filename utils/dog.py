
def dog(
    learning_rate: base.ScalarOrSchedule = 1.0,
    init_step: tuple[
        Literal["distance", "learning_rate", "heuristic"], jax.typing.ArrayLike
    ] = ("heuristic", 1e-6),
    eps: jax.typing.ArrayLike = 1e-8,
    weight_decay: Optional[jax.typing.ArrayLike] = None,
    mask: Optional[Union[Any, Callable[[base.Params], Any]]] = None,
):
  r"""Distance over Gradients (DoG) optimizer.

  DoG updates parameters :math:`x_t` with stochastic gradients :math:`g_t`
  according to the update rule:

  .. math::

    \begin{align*}
      r_t &= \| x_t - x_0 \| \\
      \bar{r}_t &= \max_{k \leq t} r_k \\
      G_t &= \sum_{k \leq t} \|g_k\|^2 \\
      \eta_t &= \frac{\bar{r}_t}{\sqrt{G_t + \epsilon}} \\
      x_{t+1} & = x_{t} - \eta_t\, g_t
    \end{align*}

  Args:
    learning_rate: optional learning rate (potentially varying according to
      some predetermined scheduler).
    init_step: Initial step specification. Consists of a pair ``(tag, value)``,
      where ``value`` is a float and ``tag`` is a string, which must be one of
      ``distance``, ``learning_rate``, or ``heuristic``.
      ``distance`` sets the initial distance :math:`r_0` (:math:`r_\epsilon` in
      the paper) to the given value.
      ``learning_rate`` sets the initial learning rate :math:`\eta_0` to the
      given value.
      ``heuristic`` sets  :math:`r_0 = \alpha (1 + \|x_0\|)`, where
      :math:`\alpha` is the given value. The suggested value of :math:`\alpha`
      is 1e-6, unless the model uses batch normalization, in which case the
      suggested value is 1e-4.
      As discussed in the paper, the value should be small enough to ensure that
      the initial update step will be small enough to not cause the model to
      diverge.
    eps: epsilon used for numerical stability - added to the sum of squared
      norm of gradients.
    weight_decay: Strength of the weight decay regularization.
    mask: A tree with same structure as (or a prefix of) the params PyTree,
      or a Callable that returns such a pytree given the params/updates.
      The leaves should be booleans, `True` for leaves/subtrees you want to
      apply the weight decay to, and `False` for those you want to skip. Note
      that the gradient transformations is applied to all parameters.

  Returns:
    The corresponding :class:`optax.GradientTransformation`.

  Examples:
    >>> import optax
    >>> from optax import contrib
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = contrib.dog()
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
    Objective function:  13.99...
    Objective function:  13.99...
    Objective function:  13.99...
    Objective function:  13.99...
    Objective function:  13.99...

  References:
    Ivgi et al., `DoG is SGD's Best Friend: A Parameter-Free Dynamic Step
    Size Schedule <https://arxiv.org/abs/2302.12022>`_, 2023.

  .. versionadded:: 0.2.3

  .. warning::
    The authors recommend using model averaging with this optimizer.

    This optimizer's ``init`` function should receive the actual parameters (not
    just dummy parameters) when the ``heuristic`` initial step is used.
  """
  return combine.chain(
      transform.add_decayed_weights(weight_decay, mask)
      if weight_decay is not None
      else base.identity(),
      scale_by_dog(init_step, eps),
      transform.scale_by_learning_rate(learning_rate),
  )

