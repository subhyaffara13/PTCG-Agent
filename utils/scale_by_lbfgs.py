
def scale_by_lbfgs(
    memory_size: int = 10,
    scale_init_precond: bool = True,
) -> base.GradientTransformation:
  r"""Scales updates by L-BFGS.

  L-BFGS is a quasi-Newton method that multiplies the update (gradient)
  with an approximation of the inverse Hessian. This algorithm does not need
  access to the Hessian, as this approximation is constructed from the gradient
  evaluations seen during optimization. L-BFGS is a limited-memory variant of
  the Broyden-Fletcher-Goldfarb-Shanno (BFGS) algorithm. The BFGS algorithm
  requires storing a matrix of size :math:`p \times p` with :math:`p` the
  dimension of the parameters.
  The limited variant circuments this issue by computing the approximation of
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
  a memory buffer.

  The present function just outputs the LBFGS direction :math:`P_k u_k`.
  It can be chained with a linesearch ensuring sufficient decrease and low
  curvature, such as a zoom linesearch. The linesearch computes a stepsize
  :math:`\eta_k`, such that the updated parameters
  (using :func:`optax.apply_updates`) take the form
  :math:`w_{k+1} = w_k - \eta_k P_k u_k`.

  Args:
    memory_size: number of past parameters, gradients/updates to keep in memory
      to approximate the Hessian inverse.
    scale_init_precond: whether to use a scaled identity as the initial
      preconditioner, see formula of :math:`\gamma_k` above.

  Returns:
    A :class:`optax.GradientTransformation` object.

  References:
    Algorithms 7.4, 7.5 (page 199) of Nocedal et al, `Numerical Optimization
    <https://www.math.uci.edu/~qnie/Publications/NumericalOptimization.pdf>`_,
    1999

    Liu et al., `On the limited memory BFGS method for large scale optimization
    <https://users.iems.northwestern.edu/~nocedal/PDFfiles/limited-memory.pdf>`_,
    1989.

  .. note::
    We initialize the scaling of the identity as a capped reciprocal of the
    gradient norm. This avoids wasting linesearch iterations for the first step
    by taking into account the magnitude of the gradients. In other words, we
    constrain the trust-region of the first step to an Euclidean ball of radius
    1 at the first iteration. The choice of :math:`\gamma_0` is not detailed in
    the references above, so this is a heuristic choice.
  """
  if memory_size < 1:
    raise ValueError('memory_size must be >= 1')

  def init_fn(params: base.Params) -> ScaleByLBFGSState:
    # diff_params_memory and diff_updates_memory represent tuple/list of trees
    # Since we cannot access the element of a tuple using a traced index such
    # as memory_idx below, we instantiate them by stacking leaves.
    # We can then access the ith element of the underlying tuple/list
    # represented by e.g. diff_params_memory through the ith stacked
    # element in the leaves, see update_fn below for practical examples.
    stacked_zero_params = jax.tree.map(
        lambda leaf: jnp.zeros((memory_size,) + leaf.shape, dtype=leaf.dtype),
        params,
    )
    return ScaleByLBFGSState(
        count=jnp.asarray(0, dtype=jnp.int32),
        params=optax.tree.zeros_like(params),
        updates=optax.tree.zeros_like(params),
        diff_params_memory=stacked_zero_params,
        diff_updates_memory=stacked_zero_params,
        weights_memory=jnp.zeros(memory_size),
    )

  def update_fn(
      updates: base.Updates, state: ScaleByLBFGSState, params: base.Params
  ) -> tuple[base.Updates, ScaleByLBFGSState]:
    # Essentially memory_idx is the iteration k (modulo the memory size)
    # and prev_memory_idx is k-1 (modulo the memory size).
    memory_idx = state.count % memory_size
    prev_memory_idx = (state.count - 1) % memory_size

    # We first update the preconditioner and then preconditon the updates.
    # That way, we can chain this function with a linesearch to update the
    # preconditioner only once a valid stepsize has been found by the linesearch
    # and the step has been done.

    # 1. Updates the memory buffers given fresh params and gradients/updates
    diff_params = optax.tree.sub(params, state.params)
    diff_updates = optax.tree.sub(updates, state.updates)
    vdot_diff_params_updates = optax.tree.real(
        optax.tree.vdot(diff_updates, diff_params)
    )
    weight = jnp.where(
        vdot_diff_params_updates == 0.0, 0.0, 1.0 / vdot_diff_params_updates
    )
    # params_diff, updates_diff, weight depend on differences of parameters
    # that are not defined at the first iteration. Hence we keep them at 0 if
    # state.count = 0.
    diff_params, diff_updates, weight = jax.tree.map(
        lambda x: jnp.where(state.count > 0, x, jnp.zeros_like(x)),
        (diff_params, diff_updates, weight),
    )
    diff_params_memory, diff_updates_memory, weights_memory = jax.tree.map(
        lambda x, y: x.at[prev_memory_idx].set(y),
        (
            state.diff_params_memory,
            state.diff_updates_memory,
            state.weights_memory,
        ),
        (diff_params, diff_updates, weight),
    )

    # 2. Compute scaling of the identity matrix (gamma_k in the formula above)
    # used to initialize the approximation of the inverse through the memory
    # buffer.
    if scale_init_precond:
      numerator = optax.tree.real(optax.tree.vdot(diff_updates, diff_params))
      denominator = optax.tree.norm(diff_updates, squared=True)
      identity_scale = jnp.where(
          denominator > 0.0, numerator / denominator, 1.0
      )
      # For the very first step of the algorithm, we consider scaling by a
      # capped reciprocal of the gradient norm, see note in the docstring.
      update_norm = optax.tree.norm(jax.lax.stop_gradient(updates))
      capped_inv_norm = jnp.minimum(1.0, 1.0 / update_norm)
      identity_scale = jnp.where(
          state.count > 0, identity_scale, capped_inv_norm
      )
    else:
      identity_scale = 1.0

    # 3. Computes the matrix vector product P_k u_k by decomposing P_k in the
    # associated rank one matrices and perform the associated vector operations
    precond_updates = _precondition_by_lbfgs(
        updates,
        diff_params_memory,
        diff_updates_memory,
        weights_memory,
        identity_scale,
        memory_idx,
    )
    return precond_updates, ScaleByLBFGSState(
        count=numerics.safe_increment(state.count),
        params=params,
        updates=updates,
        diff_params_memory=diff_params_memory,
        diff_updates_memory=diff_updates_memory,
        weights_memory=weights_memory,
    )

  return base.GradientTransformation(init_fn, update_fn)

