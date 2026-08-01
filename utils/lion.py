
def lion(
    learning_rate: base.ScalarOrSchedule,
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.99,
    mu_dtype: Optional[Any] = None,
    weight_decay: base.ScalarOrSchedule = 1e-3,
    mask: Optional[Union[Any, Callable[[base.Params], Any]]] = None,
) -> base.GradientTransformationExtraArgs:
  r"""The Lion optimizer.

  Lion is discovered by symbolic program search. Unlike most adaptive optimizers
  such as AdamW, Lion only tracks momentum, making it more memory-efficient.
  The update of Lion is produced through the sign operation, resulting in a
  larger norm compared to updates produced by other optimizers such as SGD and
  AdamW. A suitable learning rate for Lion is typically 3-10x smaller than that
  for AdamW, the weight decay for Lion should be in turn 3-10x larger than that
  for AdamW to maintain a similar strength (lr * wd).

  Let :math:`\alpha_t` represent the learning rate and :math:`\beta_1, \beta_2`,
  represent the arguments ``b1`` and ``b2`` respectively. The learning rate is
  indexed by :math:`t` since the learning rate may also be provided by a
  schedule function. Let :math:`\lambda` be the weight decay and
  :math:`\theta_t` the parameter vector at time :math:`t`.

  The ``init`` function of this optimizer initializes an internal state
  :math:`S_0 := (m_0) = (0)`, representing the intial estimate for the
  first moment. In practice these values are stored as pytrees
  containing all zeros, with the same shape as the model updates.
  At step :math:`t`, the ``update`` function of this optimizer takes as
  arguments the incoming gradients :math:`g_t`, the optimizer state :math:`S_t`
  and the parameters :math:`\theta_t` and computes updates :math:`u_t` and
  new state :math:`S_{t+1}`. Thus, for :math:`t > 0`, we have,

  .. math::

    \begin{align*}
      c_t &\leftarrow \beta_1 \cdot m_{t-1} + (1-\beta_1) \cdot g_t \\
      u_t &\leftarrow -\alpha_t \cdot \left( sign \left( c_t \right) +
      \lambda \theta_{t} \right)\\
      m_t &\leftarrow \beta_2 \cdot m_{t-1} + (1-\beta_2) \cdot g_t \\
      S_t &\leftarrow (m_t).
    \end{align*}

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    b1: Rate to combine the momentum and the current gradient.
    b2: Exponential decay rate to track the momentum of past gradients.
    mu_dtype: Optional `dtype` to be used for the first order accumulator; if
      `None` then the `dtype` is inferred from `params` and `updates`.
    weight_decay: Strength of the weight decay regularization. Note that this
      weight decay is multiplied with the learning rate. This is consistent with
      other frameworks such as PyTorch, but different from (Loshchilov et al,
      2019) where the weight decay is only multiplied with the "schedule
      multiplier", but not the base learning rate.
    mask: A tree with same structure as (or a prefix of) the params PyTree, or a
      Callable that returns such a pytree given the params/updates. The leaves
      should be booleans, `True` for leaves/subtrees you want to apply the
      weight decay to, and `False` for those you want to skip. Note that the
      Adam gradient transformations are applied to all parameters.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.lion(learning_rate=0.003)
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
    Objective function: 1.39E+01
    Objective function: 1.39E+01
    Objective function: 1.39E+01
    Objective function: 1.38E+01

  References:
    Chen et al, `Symbolic Discovery of Optimization Algorithms
    <https://arxiv.org/abs/2302.06675>`_, 2023
  """
  return combine.chain(
      transform.scale_by_lion(b1=b1, b2=b2, mu_dtype=mu_dtype),
      transform.add_decayed_weights(weight_decay, mask),
      transform.scale_by_learning_rate(learning_rate),
  )

