
def amsgrad(
    learning_rate: base.ScalarOrSchedule,
    b1: jax.typing.ArrayLike = 0.9,
    b2: jax.typing.ArrayLike = 0.999,
    eps: jax.typing.ArrayLike = 1e-8,
    eps_root: jax.typing.ArrayLike = 0.0,
    mu_dtype: Optional[Any] = None,
    bias_correction_mu: bool = True,
    bias_correction_nu: bool = True,
) -> base.GradientTransformationExtraArgs:
  """The AMSGrad optimizer.

  The original Adam can fail to converge to the optimal solution in some cases.
  AMSGrad guarantees convergence by using a long-term memory of past gradients.

  Args:
    learning_rate: A global scaling factor, either fixed or evolving along
      iterations with a scheduler, see :func:`optax.scale_by_learning_rate`.
    b1: Exponential decay rate to track the first moment of past gradients.
    b2: Exponential decay rate to track the second moment of past gradients.
    eps: A small constant applied to denominator outside of the square root (as
      in the Adam paper) to avoid dividing by zero when rescaling.
    eps_root: A small constant applied to denominator inside the square root (as
      in RMSProp), to avoid dividing by zero when rescaling. This is needed for
      instance when computing (meta-)gradients through Adam.
    mu_dtype: Optional `dtype` to be used for the first order accumulator; if
      `None` then the `dtype` is inferred from `params` and `updates`.
    bias_correction_mu: Whether to apply bias correction to the first moment
      estimate. Set to ``False`` to match the original AMSGrad paper.
    bias_correction_nu: Whether to apply bias correction to the second moment
      estimate before taking the elementwise maximum (``nu_max``). Set to
      ``False`` to match the original AMSGrad paper.

  Returns:
    The corresponding :class:`optax.GradientTransformationExtraArgs`.

  Examples:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)  # simple quadratic function
    >>> solver = optax.amsgrad(learning_rate=0.003)
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
    Reddi et al, `On the Convergence of Adam and Beyond
    <https://openreview.net/forum?id=ryQu7f-RZ>`_, 2023
  """
  return combine.chain(
      transform.scale_by_amsgrad(
          b1=b1,
          b2=b2,
          eps=eps,
          eps_root=eps_root,
          mu_dtype=mu_dtype,
          bias_correction_mu=bias_correction_mu,
          bias_correction_nu=bias_correction_nu,
      ),
      transform.scale_by_learning_rate(learning_rate),
  )

