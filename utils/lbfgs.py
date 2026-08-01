
def lbfgs(
    learning_rate: Optional[base.ScalarOrSchedule] = None,
    memory_size: int = 10,
    scale_init_precond: bool = True,
    linesearch: Optional[
        Union[base.GradientTransformationExtraArgs, base.GradientTransformation]
    ] = _linesearch.scale_by_zoom_linesearch(
        max_linesearch_steps=20, initial_guess_strategy='one'
    ),
) -> base.GradientTransformationExtraArgs:
  r"""L-BFGS optimizer.

  L-BFGS is a quasi-Newton method that multiplies the update (gradient)
  with an approximation of the inverse Hessian. This algorithm does not need
  access to the Hessian, as this approximation is constructed from the gradient
  evaluations seen during optimization. L-BFGS is a limited-memory variant of
  the Broyden-Fletcher-Goldfarb-Shanno (BFGS) algorithm. The BFGS algorithm
  requires storing a matrix of size :math:`p \times p` with :math:`p` the
  dimension of the parameters.
  The limited variant circumvents this issue by computing the approximation of
  the inverse using only :math:`m` (``memory_size``) past differences of
  parameters/gradients. Namely, the approximation of the Hessian inverse is
  denoted :math:`P_k = P_{k, k}`, where

  .. math::

    \begin{align*}
      P_{k, j+1} & = V_j^\top P_{k, j} V_j + \rho_j \delta w_j \delta w_j^\top
      \quad \text{for} \ j \in \{k-m, \ldots, k-1\}\\
      P_{k, k-m} & = \gamma_k I \\
      V_k & = I - \rho_k \delta u_k \delta w_k^\top \\
      \rho_k & = 1/(\delta u_k^\top \delta w_k) \\
      \delta w_k & = w_{k+1} - w_k \\
      \delta u_k & = u_{k+1} - u_k \\
      \gamma_k & =
        \begin{cases}
          (\delta w_{k-1}^\top \delta u_{k-1}) /
          (\delta u_{k-1}^\top \delta u_{k-1})
          & \text{if} \ \texttt{scale\_init\_hess} \\
          1 & \text{otherwise}
        \end{cases},
    \end{align*}

  for
  :math:`u_k` the gradients/updates at iteration :math:`k`,
  :math:`w_k` the parameters at iteration :math:`k`.

  The formula for updating :math:`P_k` is obtained by computing the optimal
  preconditioning matrix subject to some secant condition, see references
  for more details. Computing :math:`P_k u_k` can be done by a sequence of
  vector operations using past differences of parameters and gradients stored in
  a memory bufffer.

  The present function just outputs the LBFGS direction :math:`P_k u_k`.
  It can be chained with a linesearch ensuring sufficient decrease and low
  curvature, such as a zoom linesearch. The linesearch computes a stepsize
  :math:`\eta_k`, such that the updated parameters
  (using :func:`optax.apply_updates`) take the form
  :math:`w_{k+1} = w_k - \eta_k P_k u_k`.

  Args:
    learning_rate: optional global scaling factor, either fixed or evolving
      along iterations with a scheduler, see
      :func:`optax.scale_by_learning_rate`. By default the learning rate is
      handled by a linesearch.
    memory_size: number of past updates to keep in memory to approximate the
      Hessian inverse.
    scale_init_precond: whether to use a scaled identity as the initial
      preconditioner, see formula of :math:`\gamma_k` above.
    linesearch: an instance of :class:`optax.GradientTransformationExtraArgs`
      such as :func:`optax.scale_by_zoom_linesearch` that computes a
      learning rate, a.k.a. stepsize, to satisfy some criterion such as a
      sufficient decrease of the objective by additional calls to the objective.

  Returns:
    A :class:`optax.GradientTransformationExtraArgs` object.

  Example:
    >>> import optax
    >>> import jax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)
    >>> solver = optax.lbfgs()
    >>> params = jnp.array([1., 2., 3.])
    >>> print('Objective function: ', f(params))
    Objective function:  14.0
    >>> opt_state = solver.init(params)
    >>> value_and_grad = optax.value_and_grad_from_state(f)
    >>> for _ in range(2):
    ...   value, grad = value_and_grad(params, state=opt_state)
    ...   updates, opt_state = solver.update(
    ...      grad, opt_state, params, value=value, grad=grad, value_fn=f
    ...   )
    ...   params = optax.apply_updates(params, updates)
    ...   print('Objective function: {:.2E}'.format(f(params)))
    Objective function: 7.52E+00
    Objective function: 7.46E-14

  References:
    Algorithms 7.4, 7.5 (page 199) of Nocedal et al, `Numerical Optimization
    <https://www.math.uci.edu/~qnie/Publications/NumericalOptimization.pdf>`_
    , 1999

    Liu et al., `On the limited memory BFGS method for large scale optimization
    <https://users.iems.northwestern.edu/~nocedal/PDFfiles/limited-memory.pdf>`_
    , 1989.

  .. warning::
    This optimizer is memory intensive and best used for small to medium
    scale problems.

  .. warning::
    This optimizer works best with a linesearch (current default is a
    zoom linesearch). See example above for best use in a non-stochastic
    setting, where we can recycle gradients computed by the linesearch using
    :func:`optax.value_and_grad_from_state`.

  .. note::
    We initialize the scaling of the identity as a capped reciprocal of the
    gradient norm. This avoids wasting linesearch iterations for the first step
    by taking into account the magnitude of the gradients. In other words, we
    constrain the trust-region of the first step to an Euclidean ball of radius
    1 at the first iteration. The choice of :math:`\gamma_0` is not detailed in
    the references above, so this is a heuristic choice.

  .. note:: The algorithm can support complex inputs.
  """
  if learning_rate is None:
    base_scaling = transform.scale(-1.0)
  else:
    base_scaling = transform.scale_by_learning_rate(learning_rate)
  if linesearch is None:
    linesearch = base.identity()
  return combine.chain(
      transform.scale_by_lbfgs(
          memory_size=memory_size, scale_init_precond=scale_init_precond
      ),
      base_scaling,
      linesearch,
  )

